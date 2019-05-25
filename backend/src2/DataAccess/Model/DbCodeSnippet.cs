using SharedModels.Enum;

namespace DataAccess.Model
{
    public class DbCodeSnippet : IEntityWithId
    {
        public int Id { get; set; }
        public string Code { get; set; }
        public CodeLanguage Language { get; set; }
    }
}