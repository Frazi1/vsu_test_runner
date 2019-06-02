using SharedModels.Enum;

namespace DataAccess.Model
{
    public class DbCodeRunIteration: IEntityWithId
    {
        public int Id { get; set; }
        public string ActualOutput { get; set; }
        public bool? IsValid { get; set; }
        public CodeRunStatus Status { get; set; }
        
        public int? TestingInputId { get; set; }
        public int QuestionAnswerId { get; set; }
        
        public virtual DbTestingInput TestingInput { get; set; }
        public virtual DbQuestionAnswer QuestionAnswer { get; set; }
    }
}