namespace SharedModels.DTOs
{
    public class AuthenticationResponseDto
    {
        public string AccessToken { get; set; }
        public string RefreshToken { get; set; }
    }
}