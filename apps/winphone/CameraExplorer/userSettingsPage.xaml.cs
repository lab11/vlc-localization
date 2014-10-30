using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;


namespace CameraExplorer
{
    public partial class userSettingsPage : PhoneApplicationPage
    {
        CameraExplorer.DataContext _dataContext = CameraExplorer.DataContext.Singleton;

        public userSettingsPage()
        {
            InitializeComponent();
            UserBox.DataContext = _dataContext.UserName;
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

        private void SetToAnonymous_Click(object sender, EventArgs e)
        {
            UserBox.Text = "Anonymous";
        }

        private void SetToWhite_Click(object sender, EventArgs e)
        {
            UserBox.Text = "Mrs. White";
        }

        private void SetToYellow_Click(object sender, EventArgs e)
        {
            UserBox.Text = "Colonel Mustard";
        }

        private void SetToBlue_Click(object sender, EventArgs e)
        {
            UserBox.Text = "Mrs. Peacock";
        }

        private void doneButton_Click(object sender, EventArgs e)
        {
            try
            {
                _dataContext.UserName = UserBox.Text;
                //_dataContext.UserName.Save();
                NavigationService.GoBack();
            }
            catch (Exception err)
            {
                System.Diagnostics.Debug.WriteLine("donebutton_Click error: " + err.Message);
                MessageBox.Show("Bad URL: " + err.Message);
            }
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {

        }
    }
}