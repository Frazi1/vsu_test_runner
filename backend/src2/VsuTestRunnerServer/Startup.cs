using System;
using System.Security.Claims;
using BusinessLayer.Authentication;
using DataAccess;
using Hangfire;
using Hangfire.MySql.Core;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json.Converters;
using Swashbuckle.AspNetCore.Swagger;

namespace VsuTestRunnerServer
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors();

            services.AddDbContextPool<TestRunnerDbContext>(options =>
                options.UseMySql(Configuration.GetConnectionString("db")));
            services.AddRepositories();
            services.AddBusinessServices();
            services.AddCodeExecutors(Configuration);
            services.AddWildcards();
            services.AddValidators();
            services.AddHangfire(x =>
                x.UseStorage(new MySqlStorage(Configuration.GetConnectionString("Hangfire")))
            );
            services.AddHangfireServer();
            services.AddJwtAuthentication(Configuration);
            services.AddHttpContextAccessor();
            services.AddScoped<ICurrentUser, CurrentUser>(provider => GetUser(provider)());

            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_2)
                .AddJsonOptions(options => { options.SerializerSettings.Converters.Add(new StringEnumConverter()); });

            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new Info {Title = "Test runner API", Version = "v1"});
            });
        }

        private static Func<CurrentUser> GetUser(IServiceProvider provider)
        {
            return () =>
            {
                var httpContextAccessor = provider.GetService<IHttpContextAccessor>();
                var claims = httpContextAccessor?.HttpContext?.User;
                if (claims == null || !claims.Identity.IsAuthenticated)
                    return null;

                var user = new CurrentUser(
                    int.Parse(claims.FindFirstValue(CustomClaimTypes.UserId)),
                    claims.FindFirstValue(ClaimTypes.Email),
                    claims.FindFirstValue(ClaimTypes.Name),
                    new string[] { });
                return user;
            };
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseCors(x => x
                .AllowAnyOrigin()
                .AllowAnyMethod()
                .AllowAnyHeader());

            app.UseAuthentication();

            app.UseMvc();
            app.UseHangfireDashboard();
            app.UseSwagger();
            app.UseSwaggerUI(c => { c.SwaggerEndpoint("/swagger/v1/swagger.json", "Test runner API"); });
        }
    }
}