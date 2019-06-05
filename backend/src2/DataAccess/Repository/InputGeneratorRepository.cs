using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class InputGeneratorRepository : BaseRepository<DbInputGenerator>
    {
        private static readonly string[] UpdatePropertiesNames = {
            nameof(DbInputGenerator.Name),
            nameof(DbInputGenerator.Description),
            nameof(DbInputGenerator.CodeSnippet),
            nameof(DbInputGenerator.CallParameters),
        };
        
        public InputGeneratorRepository(TestRunnerDbContext context) : base(context)
        {
        }

        public async Task<DbInputGenerator> GetFullByIdAsync(int id)
        {
            return await Set
                .Include(g => g.CodeSnippet)
                .Include(g => g.CreatedByUser)
                .FirstAsync(g => g.Id == id);
        }

        public override Task Update(DbInputGenerator updated)
        {
            Context.Attach(updated);
            Context.Entry(updated).Property(o => o.Name).IsModified = true;                    
            Context.Entry(updated).Property(o => o.Description).IsModified = true;                    
            Context.Entry(updated).Property(o => o.CallParameters).IsModified = true;

            Context.Entry(updated.CodeSnippet).Property(o => o.Code).IsModified = true;
            Context.Entry(updated.CodeSnippet).Property(o => o.Language).IsModified = true;
            
//            Context.ChangeTracker.TrackGraph(updated, e =>
//            {
//                if (e.Entry.Entity is DbInputGenerator g)
//                {
//                    Context.Entry(g).Property(o => o.Name).IsModified = true;                    
//                    Context.Entry(g).Property(o => o.Description).IsModified = true;                    
//                    Context.Entry(g).Property(o => o.CallParameters).IsModified = true;                    
//                }
//                if (e.Entry.Entity is DbCodeSnippet s)
//                {
//                    Context.Entry(s).Property(o => o.Code).IsModified = true;
//                    Context.Entry(s).Property(o => o.Language).IsModified = true;
//                }
//            });
            return Task.CompletedTask;
        }
    }
}