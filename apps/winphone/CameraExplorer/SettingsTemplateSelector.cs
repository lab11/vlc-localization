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
    /// Settings template selector selects the appropriate UI control tempalate for a parameter.
    /// See the SettingsPage.xaml file for the template declarations.
    /// </summary>
    public class SettingsTemplateSelector : ContentControl
    {
        public DataTemplate ArrayParameterTemplate { get; set; }
        public DataTemplate RangeParameterTemplate { get; set; }
        public DataTemplate UnsupportedParameterTemplate { get; set; }

        protected override void OnContentChanged(object oldContent, object newContent)
        {
            ContentTemplate = SelectTemplate(newContent);

            base.OnContentChanged(oldContent, newContent);
        }

        /// <summary>
        /// If parameter is not supported or modifiable, it is not displayed in the UI, and thus
        /// the unsupported parameter template is used. If Parameter is supported and modifiable,
        /// then the decision between the template is done on basis of the type of the parameter.
        /// </summary>
        /// <param name="item">Parameter instance</param>
        public DataTemplate SelectTemplate(object item)
        {
            Parameter parameter = item as Parameter;

            if (parameter.Supported && parameter.Modifiable)
            {
                if (parameter is ArrayParameter)
                {
                    return ArrayParameterTemplate;
                }
                else
                {
                    return RangeParameterTemplate;
                }
            }
            else
            {
                return UnsupportedParameterTemplate;
            }
        }
    }
}