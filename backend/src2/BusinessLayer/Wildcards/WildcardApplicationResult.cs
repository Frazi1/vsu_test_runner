namespace BusinessLayer.Wildcards
{
    public class WildcardApplicationResult
    {
        public string TransformedInput { get; set; }

        public WildcardApplicationResult(string transformedInput)
        {
            TransformedInput = transformedInput;
        }
    }
}