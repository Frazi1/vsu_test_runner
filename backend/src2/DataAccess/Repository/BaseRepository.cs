using System.Collections.Generic;
using System.Threading.Tasks;
using DataAccess.Model;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    public class BaseRepository<T> where T : class, IEntityWithId
    {
        protected TestRunnerDbContext Context { get; }
        protected DbSet<T> Set => Context.Set<T>();

        protected BaseRepository(TestRunnerDbContext context)
        {
            Context = context;
        }

        public async Task<List<T>> GetAllAsync() => await Context.Set<T>().ToListAsync();

        public async Task<T> GetByIdAsync(int id) => await Context.Set<T>().FirstAsync(e => e.Id == id);

        public void Add(T entity) => Context.Add(entity);
        public void Remove(T entity) => Context.Remove(entity);

        public async Task SaveChangesAsync() => await Context.SaveChangesAsync();

        public virtual Task Update(T updated)
        {
            Context.Update(updated);
            return Task.CompletedTask;
        }
    }
}