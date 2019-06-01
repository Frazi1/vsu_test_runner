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
using BusinessLayer.Wildcards;
using DataAccess.Repository;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
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
                .GetAssembly(typeof(BaseRepository<>))
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
                    .Select(conf => (Language: conf.LanguageIdentifier,
                        Executor: conf.CompilationRequired
                            ? new CompileCodeExecutor(conf, pipeLineTasksProvider)
                            : new CodeExecutor(conf, pipeLineTasksProvider)))
                    .ToImmutableDictionary(a => a.Language, a => a.Executor);
                return new ExecutorsProvider(executors);
            });
        }

        public static void AddWildcards(this IServiceCollection services)
        {
            services.AddSingleton<WildcardsFactory>();
        }
    }
}