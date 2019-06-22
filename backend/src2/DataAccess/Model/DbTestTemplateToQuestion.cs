namespace DataAccess.Model
{
    public class DbTestTemplateToQuestion
    {
        public int TestTemplateId { get; set; }
        public int QuestionTemplateId { get; set; }

        public virtual DbTestTemplate TestTemplate { get; set; }
        public virtual DbQuestionTemplate QuestionTemplate { get; set; }
        
    }
}