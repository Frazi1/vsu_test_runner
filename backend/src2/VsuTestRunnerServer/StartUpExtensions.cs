using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Reflection;
using BusinessLayer;
using BusinessLayer.Executors;
using BusinessLayer.Services;
using DataAccess.Repository;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

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
                .GetAssembly(typeof(BaseRepository<>))
                .GetTypes()
                .Where(t => t.Name.EndsWith("Repository"))
                .Where(t => !t.IsAbstract))
            {
                services.AddScoped(type);
            }
        }

        public static void AddBusinessServices(this IServiceCollection services, IConfiguration configuration)
        {
            foreach (Type type in GetInheritors<BaseService>())
                services.AddScoped(type);

            services.AddCodeExecutors(configuration);
        }

        private static void AddCodeExecutors(this IServiceCollection services, IConfiguration configuration)
        {
            var languagesConfigs = configuration.GetSection("LanguageSettings")
                .GetChildren()
                .Select(sect => sect.Get<LanguageConfiguration>())
                .Select(config => (
                    config.LanguageIdentifier,
                    Executor: config.CompilationRequired ? new CompileCodeExecutor(config) : new CodeExecutor(config))
                )
                .ToImmutableDictionary(e => e.LanguageIdentifier, e=> e.Executor);

            var executorsProvider = new ExecutorsProvider(languagesConfigs);

            services.AddSingleton(executorsProvider);
        }
    }
}