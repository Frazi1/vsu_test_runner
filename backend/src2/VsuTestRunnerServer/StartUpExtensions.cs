using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using BusinessLayer;
using BusinessLayer.Executors;
using BusinessLayer.Executors.PipelineTasks;
using BusinessLayer.Services;
using BusinessLayer.Validators;
using BusinessLayer.Wildcards;
using DataAccess.Repository;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.IdentityModel.Tokens;
using SharedModels;
using SharedModels.DTOs;

namespace VsuTestRunnerServer
{
    public static class StartUpExtensions
    {
        private static IEnumerable<Type> GetInheritors<TTarget>() => GetInheritors(typeof(TTarget));

        private static IEnumerable<Type> GetInheritors(Type type) =>
            Assembly
                .GetAssembly(type)
                .GetTypes()
                .Where(t => t.IsSubclassOf(type))
                .Where(t => !t.IsAbstract);


        public static void AddRepositories(this IServiceCollection services)
        {
            foreach (var type in Assembly
                .GetAssembly(typeof(BaseEntityWithIdRepository<>))
                .GetTypes()
                .Where(t => t.Name.EndsWith("Repository"))
                .Where(t => !t.IsAbstract))
            {
                services.AddScoped(type);
            }
        }

        public static void AddBusinessServices(this IServiceCollection services)
        {
            foreach (Type type in GetInheritors<BaseService>())
                services.AddScoped(type);
        }

        public static void AddCodeExecutors(this IServiceCollection services, IConfiguration configuration)
        {
            var languagesDict = configuration.GetSection("LanguageSettings")
                .GetChildren()
                .Select(sect => sect.Get<LanguageConfiguration>())
                .ToImmutableDictionary(e => e.LanguageIdentifier);

            services.AddSingleton<IImmutableDictionary<LanguageIdentifier, LanguageConfiguration>>(languagesDict);
            services.AddSingleton<PipeLineTasksProvider>(
                provider => new PipeLineTasksProvider(configuration.GetValue<string>("WorkDir"))
            );
            services.AddSingleton<ExecutorsProvider>(provider =>
            {
                var languages = provider.GetService<IImmutableDictionary<LanguageIdentifier, LanguageConfiguration>>();
                var pipeLineTasksProvider = provider.GetService<PipeLineTasksProvider>();

                var executors = languages
                    .Select(l => l.Value)
                    .Select(conf =>
                        (Language: conf.LanguageIdentifier, Executor: new CodeExecutor(conf, pipeLineTasksProvider)))
                    .ToImmutableDictionary(a => a.Language, a => a.Executor);
                return new ExecutorsProvider(executors);
            });
        }

        public static void AddWildcards(this IServiceCollection services)
        {
            services.AddSingleton<WildcardsFactory>();
        }

        public static void AddValidators(this IServiceCollection services)
        {
            services.AddSingleton<ITestValidator, LineByLineValidator>();
            services.AddSingleton<IReadOnlyCollection<ITestValidator>>(provider =>
                provider.GetServices<ITestValidator>().ToImmutableList());
        }

        public static IServiceCollection AddJwtAuthentication(this IServiceCollection services,
            IConfiguration configuration)
        {
            var key = new SigningSymmetricKey(configuration.GetValue<string>("Authentication:PrivateKey"));
            services.AddSingleton<IJwtSigningEncodingKey>(key);

            var decodingKey = (IJwtSigningDecodingKey) key;
            const string jwtSchemeName = "JwtBearer";
            services.AddAuthentication(options =>
                {
                    options.DefaultScheme = jwtSchemeName;
                    options.DefaultChallengeScheme = jwtSchemeName;
                })
                .AddJwtBearer(jwtSchemeName, jwtBearerOptions =>
                {
                    jwtBearerOptions.TokenValidationParameters = new TokenValidationParameters
                    {
                        ValidateIssuerSigningKey = true,
                        IssuerSigningKey = decodingKey.GetKey(),
                        ValidateIssuer = true,
                        ValidIssuer = "TestRunnerServer",
                        ValidateAudience = true,
                        ValidAudiences = new[] {"TestRunnerClient"},
                        ValidateLifetime = true,
                        ClockSkew = TimeSpan.FromSeconds(5)
                    };
                });

            return services;
        }
    }
}