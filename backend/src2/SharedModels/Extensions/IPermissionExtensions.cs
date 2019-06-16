using System;
using SharedModels.DTOs;

namespace SharedModels.Extensions
{
    public static class PermissionExtensions
    {
        public static void CopyPermissionsTo(this IPermission permission, IPermission other)
        {
            if (permission == null)
            {
                throw new ArgumentNullException(nameof(permission));
            }

            other.Read = permission.Read;
            other.Write = permission.Write;
            other.Execute = permission.Execute;
        }
    }
}