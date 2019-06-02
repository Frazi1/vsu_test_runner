using BusinessLayer.Wildcards;
using NUnit.Framework;

namespace Tests
{
    [TestFixture]
    public class SolutionCodeExtractorWildcardTests
    {
        private const string Replacement = "Write code here...";

        public SolutionCodeExtractorWildcard Wildcard { get; set; }

        [SetUp]
        public void Setup()
        {
            Wildcard = new SolutionCodeExtractorWildcard("//", Replacement);
        }

        [Test]
        public void ReplaceEmpty()
        {
            const string x = "//SolutionStart//SolutionEnd";
            RunTestWithInput(x);
        }

        private void RunTestWithInput(string input)
        {
            string res = Wildcard.Apply(input).TransformedInput;
            Assert.AreEqual($"//{Replacement}", res);
        }

        [Test]
        public void ReplaceWithText()
        {
            const string x = "//SolutionStart hello this is my code to replace //SolutionEnd";
            RunTestWithInput(x);
        }

        [Test]
        public void ReplaceWithNewLine()
        {
            const string x = @"//SolutionStart
hello this is my code to replace    
  //SolutionEnd";
            RunTestWithInput(x);
        }
    }
}