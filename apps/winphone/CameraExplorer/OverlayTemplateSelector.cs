/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

using System.Windows;
using System.Windows.Controls;

namespace CameraExplorer
{
    /// <summary>
    /// Overlay template selector selects the overlay template for a parameter. See the
    /// MainPage.xaml file for the template declarations.
    /// </summary>
    public class OverlayTemplateSelector : ContentControl
    {
        public DataTemplate ParameterWithoutOverlayTemplate { get; set; }
        public DataTemplate ParameterWithOverlayTemplate { get; set; }

        protected override void OnContentChanged(object oldContent, object newContent)
        {
            ContentTemplate = SelectTemplate(newContent);

            base.OnContentChanged(oldContent, newContent);
        }

        /// <summary>
        /// If parameter has OverlaySource set then a template with an Image XAML control is selected,
        /// otherwise a template without an Image control is used.
        /// </summary>
        /// <param name="item">Parameter instance</param>
        public DataTemplate SelectTemplate(object item)
        {
            if ((item as Parameter).OverlaySource != null)
            {
                return ParameterWithOverlayTemplate;
            }
            else
            {
                return ParameterWithoutOverlayTemplate;
            }
        }
    }
}
