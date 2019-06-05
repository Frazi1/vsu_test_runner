using Microsoft.IdentityModel.Tokens;

namespace SharedModels
{
    public interface IJwtSigningEncodingKey
    {
        string SigningAlgorithm { get; }
        SecurityKey GetKey();
    }
    
    public interface IJwtSigningDecodingKey
    {
        SecurityKey GetKey();
    }
}