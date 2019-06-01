namespace Utils
{
    public static class StringExtensions
    {
        public static string OrIfNullOrEmpty(this string first, string second)
            => !string.IsNullOrEmpty(first) ? first : second;
    }
}