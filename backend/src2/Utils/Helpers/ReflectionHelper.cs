using System;

namespace Utils.Helpers
{
    public static class ReflectionHelper
    {
        public static void SetPropertyValue(this object obj, string propertyName, object newValue)
        {
            var propertyInfo = obj.GetType().GetProperty(propertyName);
            if (propertyInfo == null)
            {
                throw new ArgumentNullException(nameof(propertyInfo));
            }

            propertyInfo.SetValue(obj, newValue);
        }
    }
}