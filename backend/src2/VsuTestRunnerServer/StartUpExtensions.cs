using BusinessLayer.Services;
using DataAccess.Repository;
using Microsoft.Extensions.DependencyInjection;

namespace VsuTestRunnerServer
{
    public static class StartUpExtensions
    {
        public static void AddRepositories(this IServiceCollection services)
        {
            services.AddScoped<TestTemplateRepository>();
        }

        public static void AddBusinessServices(this IServiceCollection services)
        {
            services.AddScoped<TemplateService>();
        }
        
    }
}