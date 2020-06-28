using System.Collections.Generic;
using System.Threading.Tasks;
using DataAccess.Repository.Interfaces;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class Repository : IRepository
    {
        protected readonly TestRunnerDbContext Context;

        public Repository(TestRunnerDbContext context)
        {
            Context = context;
        }

        public DbSet<T> Set<T>() where T : class => Context.Set<T>();

        public void Add<T>(T entity) => Context.Add(entity);

        public void AddRange<T>(IEnumerable<T> items) => Context.AddRange(items);

        public Task SaveChangesAsync() => Context.SaveChangesAsync();
    }
}