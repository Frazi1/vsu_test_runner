namespace SharedModels.DTOs
{
    public class Permission : IPermission
    {
        public bool Read { get; set; }
        public bool Write { get; set; }
        public bool Execute { get; set; }
    }
}