﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Threading.Tasks;
using DataAccess.Model;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    public class BaseRepository<T>: Repository where T : class

    {
        protected BaseRepository(TestRunnerDbContext context) : base(context)
        {
        }

        protected DbSet<T> Set => Context.Set<T>();

        public async Task<bool> AnyAsync(Expression<Func<T, bool>> expression) => await Set.AnyAsync(expression);

        public async Task<List<T>> GetAllAsync() => await Context.Set<T>().ToListAsync();

        public async Task<List<T>> GetAllAsync(Expression<Func<T, bool>> expression)
            => await Context.Set<T>().Where(expression).ToListAsync();

        public async Task<T> GetFirstAsync(Expression<Func<T, bool>> expression) =>
            await Context.Set<T>().FirstAsync(expression);

        public async Task<T> GetFirstOrDefaultAsync(Expression<Func<T, bool>> expression)
            => await Context.Set<T>().FirstOrDefaultAsync(expression);

        public void Remove(T entity) => Context.Remove(entity);
        
        public virtual Task Update(T updated)
        {
            Context.Update(updated);
            return Task.CompletedTask;
        }
    }

    public class BaseEntityWithIdRepository<T> : BaseRepository<T> where T : class, IEntityWithId
    {
        protected BaseEntityWithIdRepository(TestRunnerDbContext context)
            : base(context)
        {
        }

        public async Task<List<T>> GetByIdsAsync(ICollection<int> ids) =>
            await Set.Where(u => ids.Contains(u.Id)).ToListAsync();

        public async Task<T> GetByIdAsync(int id) => await GetFirstAsync(e => e.Id == id);
    }
}