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
    public partial class UploadSettingsPage : PhoneApplicationPage
    {
        CameraExplorer.DataContext _dataContext = CameraExplorer.DataContext.Singleton;

        public UploadSettingsPage()
        {
            InitializeComponent();
            UrlBox.DataContext = _dataContext.UploadUrl;
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

        private void SetToPfet_Click(object sender, EventArgs e)
        {
            UrlBox.Text = "http://pfet-v2.eecs.umich.edu:4908/img/";
            //_dataContext.UploadUrl.Url = new Uri("http://pfet-v2.eecs.umich.edu:4908/img/");
        }

        private void SetToCapacitor_Click(object sender, EventArgs e)
        {
            UrlBox.Text = "http://capacitor.eecs.umich.edu:4908/img/";
            //_dataContext.UploadUrl.Url = new Uri("http://capacitor.eecs.umich.edu:4908/img/");
        }

        private void SetToMemristor_Click(object sender, EventArgs e)
        {
            UrlBox.Text = "http://memristor-v1.eecs.umich.edu:4908/img/";
        }

        private void SetToNinja_Click(object sender, EventArgs e)
        {
            UrlBox.Text = "http://ninja.eecs.umich.edu:4908/img/";
        }

        private void SetToPatbook_Click(object sender, EventArgs e)
        {
            UrlBox.Text = "http://patbook.eecs.umich.edu:4908/img/";
        }

        private void doneButton_Click(object sender, EventArgs e)
        {
            try
            {
                _dataContext.UploadUrl.Url = new Uri(UrlBox.Text);
                _dataContext.UploadUrl.Save();
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