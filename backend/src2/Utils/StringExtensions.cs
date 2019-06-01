namespace Utils
{
    public static class StringExtensions
    {
        public static string OrIfNullOrEmpty(this string first, string second)
            => !string.IsNullOrEmpty(first) ? first : second;

        public static string RemoveFromEndSafe(this string input, int number)
            => input.Length < number ? input : input.Remove(input.Length - number);
    }
}