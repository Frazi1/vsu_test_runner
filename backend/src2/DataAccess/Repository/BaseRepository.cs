using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
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

        public async Task<bool> AnyAsync(Expression<Func<T, bool>> expression) => await Set.AnyAsync(expression);

        public async Task<List<T>> GetAllAsync() => await Context.Set<T>().ToListAsync();
        public async Task<List<T>> GetByIdsAsync(ICollection<int> ids) =>
            await Set.Where(u => ids.Contains(u.Id)).ToListAsync();

        public async Task<T> GetByIdAsync(int id) => await GetFirstAsync(e => e.Id == id);

        public async Task<T> GetFirstAsync(Expression<Func<T, bool>> expression) =>
            await Context.Set<T>().FirstAsync(expression);

        public async Task<T> GetFirstOrDefaultAsync(Expression<Func<T, bool>> expression)
            => await Context.Set<T>().FirstOrDefaultAsync(expression);

        public void Add(T entity) => Context.Add(entity);
        public void AddRange(IEnumerable<T> items) => Context.AddRange(items);
        public void Remove(T entity) => Context.Remove(entity);

        public async Task SaveChangesAsync() => await Context.SaveChangesAsync();

        public virtual Task Update(T updated)
        {
            Context.Update(updated);
            return Task.CompletedTask;
        }
    }
}