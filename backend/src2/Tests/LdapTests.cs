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
            var res = _query.GetUsers("dc=example,dc=com", "objectClass=person", new []{"uid", "mail"});
            var ldapEntries = res.ToList();
            Assert.IsTrue( ldapEntries.Any());
        }
    }
}