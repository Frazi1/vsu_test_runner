using System.Text.RegularExpressions;

namespace BusinessLayer.Wildcards
{
    public abstract class BinaryWildcard : IWildcard
    {
        private readonly string _start;
        private readonly string _end;

        protected BinaryWildcard(string start, string end)
        {
            _start = start;
            _end = end;
        }

        protected string ReplaceMatches(string input, MatchEvaluator evaluator)
        {
            return Regex.Replace(input, $"{_start}(.*?){_end}", evaluator, RegexOptions.Singleline);
        }

        public abstract WildcardApplicationResult Apply(string input);
    }
}