namespace SharedModels.DTOs
{
    public interface IPermission
    {
        bool Read { get; set; }
        bool Write { get; set; }
        bool Execute { get; set; }
    }
}