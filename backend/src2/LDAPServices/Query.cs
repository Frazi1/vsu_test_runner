﻿using Novell.Directory.Ldap;

namespace LDAPServices
{
    public class Query
    {
        private LdapConnection _connection;

        public Query(string host, int port, string dn, string password)
        {
            _connection = new LdapConnection();
            _connection.Connect(host, port);
            _connection.Bind(dn, password);
        }

        public LdapSearchResults GetUsers(string baseSearch, string searchFilter)
        {
            var res = _connection.Search(baseSearch, LdapConnection.SCOPE_ONE, searchFilter, null, false);
            int c = res.Count;
            return res;
        }
    }
}