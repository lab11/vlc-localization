/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using Microsoft.Phone.Controls;
using Windows.Phone.Media.Capture;
using Microsoft.Phone.Shell;

namespace CameraExplorer
{
    /// <summary>
    /// Settings page displays UI controls for all instantiated parameter objects.
    /// </summary>
    public partial class SettingsPage : PhoneApplicationPage
    {
        CameraExplorer.DataContext _dataContext = CameraExplorer.DataContext.Singleton;

        public SettingsPage()
        {
            InitializeComponent();

            DataContext = _dataContext;
        }

        /// <summary>
        /// When navigating to this page, if camera has not been initialized (for example returning from
        /// tombstoning), application will navigate directly back to the main page.
        /// </summary>
        protected override void OnNavigatedTo(System.Windows.Navigation.NavigationEventArgs e)
        {
            if (_dataContext.Device == null)
            {
                NavigationService.GoBack();
            }

            base.OnNavigatedTo(e);
        }

        /// <summary>
        /// Clicking on the reset button causes SetDefault to be called on all parameter instances.
        /// </summary>
        private void resetItem_Click(object sender, EventArgs e)
        {
            SetScreenButtonsEnabled(false);

            foreach (Parameter i in _dataContext.Parameters)
            {
                i.SetDefault();
            }

            SetScreenButtonsEnabled(true);
        }

        /// <summary>
        /// Enables or disabled on-screen controls.
        /// </summary>
        /// <param name="enabled">True to enable controls, false to disable controls.</param>
        private void SetScreenButtonsEnabled(bool enabled)
        {
            foreach (ApplicationBarIconButton b in ApplicationBar.Buttons)
            {
                b.IsEnabled = enabled;
            }
        }
    }
}