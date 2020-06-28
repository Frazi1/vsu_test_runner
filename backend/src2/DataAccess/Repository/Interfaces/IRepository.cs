using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository.Interfaces
{
    public interface IRepository
    {
        DbSet<T> Set<T>() where T : class;
        void Add<T>(T entity);
        void AddRange<T>(IEnumerable<T> items);
        Task SaveChangesAsync();
    }
}