namespace BusinessLayer.Wildcards
{
    public class SolutionCodeExtractorWildcard : BinaryWildcard
    {
        private readonly string _languageComment;
        private readonly string _replacement;

        private const string Start = "SolutionStart";
        private const string End = "SolutionEnd";

        public SolutionCodeExtractorWildcard(string languageComment, string replacement)
            : base(languageComment + Start, languageComment + End)
        {
            _languageComment = languageComment;
            _replacement = replacement;
        }

        public override WildcardApplicationResult Apply(string input)
        {
            string result = ReplaceMatches(input, match => _languageComment + _replacement);
            return new WildcardApplicationResult(result);
        }
    }
}