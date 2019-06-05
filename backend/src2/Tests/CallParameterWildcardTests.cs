using BusinessLayer.Wildcards;
using NUnit.Framework;

namespace Tests
{
    public class CallParameterWildcardTests
    {
        public CallParameterWildcard Wildcard { get; set; }

        [SetUp]
        public void Setup()
        {
            Wildcard = new CallParameterWildcard("//");
        }

        [Test]
        public void ZeroCallsTest()
        {
            const string input = "Hello world";
            var res = Wildcard.GetCallParameters(input);
            Assert.IsEmpty(res.CallArguments);
        }

        [Test]
        public void OneSimpleWildcardTest()
        {
            const string input = "//@CallArg:Length";
            var res = Wildcard.GetCallParameters(input);

            Assert.IsTrue(res.CallArguments.Count == 1);
            Assert.AreEqual("Length", res.CallArguments[0].Name);
        }

        [Test]
        public void CommentSpaceWildcardTest()
        {
            const string input = "//    @CallArg:Length";
            var res = Wildcard.GetCallParameters(input);

            Assert.IsTrue(res.CallArguments.Count == 1);
            Assert.AreEqual("Length", res.CallArguments[0].Name);
        }

        [Test]
        public void OneLineTwoWildcardsTest()
        {
            const string input = "//@CallArg:Length//@CallArg:MaxSize";
            var res = Wildcard.GetCallParameters(input);

            Assert.IsTrue(res.CallArguments.Count == 2);
            Assert.AreEqual("Length", res.CallArguments[0].Name);
            Assert.AreEqual("MaxSize", res.CallArguments[1].Name);
        }

        [Test]
        public void TwoLinesTwoWildcardsTest()
        {
            const string input = @"//@CallArg:Length
//@CallArg:MaxSize";
            var res = Wildcard.GetCallParameters(input);

            Assert.IsTrue(res.CallArguments.Count == 2);
            Assert.AreEqual("Length", res.CallArguments[0].Name);
            Assert.AreEqual("MaxSize", res.CallArguments[1].Name);
        }

        [Test]
        public void CodeWithWildOneWildCardTest()
        {
            const string input = @" public static void Main(string[] args)
        {
            string x = Console.ReadLine(); // @CallArg:Length
             string res = MyFunc();
             Console.WriteLine(res);
        }";
            
            var res = Wildcard.GetCallParameters(input);
            Assert.IsTrue(res.CallArguments.Count == 1);
            Assert.AreEqual("Length", res.CallArguments[0].Name);
        }
    }
}