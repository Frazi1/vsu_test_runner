
namespace DataAccess.Model
{
    public class DbCodeSnippet : IEntityWithId
    {
        public int Id { get; set; }
        public string Code { get; set; }
        public string Language { get; set; }
    }
}