/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

namespace CameraExplorer
{
    /// <summary>
    /// Extensions class contains function extensions to existing types.
    /// </summary>
    public static class Extensions
    {
        /// <summary>
        /// Adds functionality to enumerations to print enumeration value name with
        /// camelcase letters replaced with lower case letters and spaces added between words.
        /// 
        /// For example "RedEyeReduction" becomes "Red eye reduction".
        /// </summary>
        /// <typeparam name="T">Enumeration type</typeparam>
        /// <param name="enumeration">Enumeration instance</param>
        /// <returns></returns>
        public static string EnumerationToParameterName<T>(this T enumeration)
        {
            string name = enumeration.ToString();

            for (int i = 1; i < name.Length; i++)
            {
                char c = name[i];

                if (c >= 'A' && c <= 'Z')
                {
                    name.Remove(i, 1);
                    name.Insert(i++, ((char)(c + 0x30)).ToString());
                    name.Insert(i, " ");
                }
            }

            return name;
        }
    }
}
