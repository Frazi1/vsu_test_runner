using System.Text.RegularExpressions;
using JetBrains.Annotations;

namespace BusinessLayer.Wildcards
{
    public abstract class UnaryWildcard : IWildcard
    {
        protected string LanguageComment { get; }
        protected Regex WildcardRegex { get; }

        protected UnaryWildcard(string languageComment, [RegexPattern] string regexTemplate)
        {
            LanguageComment = languageComment;
            WildcardRegex = new Regex($@"{languageComment}\s*{regexTemplate}");
        }
        public abstract WildcardApplicationResult Apply(string input);
    }
}