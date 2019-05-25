namespace DataAccess.Model
{
    public class DbTestingInput : IEntityWithId
    {
        public int Id { get; set; }
        public string Input { get; set; }
        public string ExpectedOutput { get; set; }
        public int QuestionTemplateId { get; set; }

        public virtual DbQuestionTemplate QuestionTemplate { get; set; }
    }
}