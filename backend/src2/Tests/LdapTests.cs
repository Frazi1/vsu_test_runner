using System.Linq;
using LDAPServices;
using NUnit.Framework;

namespace Tests
{
    public class LdapTests
    {
        private LDAPServices.Query _query;

        [SetUp]
        public void SetUp()
        {
            _query = new Query("ldap.forumsys.com", 389, "cn=read-only-admin,dc=example,dc=com", "password");
        }

        [Test]
        public void TestSearch()
        {
            var res = _query.GetUsers("ou=scientists,dc=example,dc=com", "");
            var ldapEntries = res.ToList();
            Assert.IsTrue( ldapEntries.Any());
        }
    }
}