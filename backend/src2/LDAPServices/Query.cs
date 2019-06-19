using System;
using Novell.Directory.Ldap;

namespace LDAPServices
{
    public class Query: IDisposable
    {
        private readonly LdapConnection _connection;

        public Query(string host, int port, string dn, string password)
        {
            _connection = new LdapConnection();
            _connection.Connect(host, port);
            _connection.Bind(dn, password);
        }

        public LdapSearchResults GetUsers(string baseSearch, string searchFilter, string[] attrs)
        {
            var res = _connection.Search(baseSearch, LdapConnection.SCOPE_ONE, searchFilter, attrs, false);
            int c = res.Count;
            return res;
        }

        public void Dispose()
        {
            _connection?.Dispose();
        }
    }
}