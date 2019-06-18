using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class ActiveDirectorySearchRequestDto
    {
        public ActiveDirectoryConnectionDataDto ConnectionData { get; set; }
        public string BaseSearch { get; set; }
        public string FilterQuery { get; set; }
        public Dictionary<string, string> UserFieldToActiveDirectoryAttributeMapping { get; set; }
    }

    public class ActiveDirectoryConnectionDataDto
    {
        public string Host { get; set; }
        public int Port { get; set; }
        public string DistinguishedName { get; set; }
        public string Password { get; set; }
    }
}