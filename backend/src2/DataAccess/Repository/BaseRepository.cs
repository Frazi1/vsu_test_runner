using System.Collections.Generic;
using System.Threading.Tasks;
using DataAccess.Model;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    public class BaseRepository<T> where T : class, IEntityWithId
    {
        private readonly TestRunnerDbContext _context;

        protected BaseRepository(TestRunnerDbContext context)
        {
            _context = context;
        }

        public async Task<List<T>> GetAllAsync() => await _context.Set<T>().ToListAsync();

        public async Task<T> GetByIdAsync(int id) => await _context.Set<T>().FirstAsync(e => e.Id == id);

        public void Add(T entity) => _context.Add(entity);
        public void Remove(T entity) => _context.Remove(entity);

        public async Task SaveChangesAsync() => await _context.SaveChangesAsync();
    }
}