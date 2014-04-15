using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using Windows.Phone.Media.Capture;

namespace CameraExplorer
{
    public abstract class UrlParameter : Parameter
    {
        private Uri _url;

        protected UrlParameter(PhotoCaptureDevice device, String name)
            : base(device, name)
        {
        }

        /// <summary>
        /// Url current value.
        /// </summary>
        public Uri Url
        {
            get
            {
                return _url;
            }
            set
            {
                if ((_url == null) || (!_url.Equals(value)))
                {
                    try
                    {
                        System.Diagnostics.Debug.WriteLine(String.Format("UrlParameter::Url::set old >>{0}<<, new >>{1}<<", _url, value));
                        _url = value;
                        System.Diagnostics.Debug.WriteLine("UrlParameter::Url::set before notify");
                        NotifyPropertyChanged("Url");
                        System.Diagnostics.Debug.WriteLine("UrlParameter::Url::set before save");
                        Save();
                    }
                    catch (Exception)
                    {
                        System.Diagnostics.Debug.WriteLine("Setting " + Name.ToLower() + " failed");
                    }
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine("UrlParameter::set URL matched. No-op.");
                }
            }
        }

        public override string ToString()
        {
            return _url.ToString();
        }

        /// <summary>
        /// Set saved value if exists, otherwise set to default.
        /// </summary>
        public override void SetSavedOrDefault()
        {
            System.Diagnostics.Debug.WriteLine("UrlParameter::SetSavedOrDefault start");
            if (!Load())
            {
                SetDefault();
            }
            System.Diagnostics.Debug.WriteLine("UrlParameter::SetSavedOrDefault end");
        }
    }

    public class UploadURLParameter : UrlParameter
    {
        public UploadURLParameter(PhotoCaptureDevice device)
            : base(device, "upload_url")
        {
        }

        /// <summary>
        /// Name of the parameter in application settings. Overridden b/c this URL is camera-independent
        /// </summary>
        new public string ParameterSettingName
        {
            get
            {
                return Name;
            }
        }

        public override void Refresh()
        {
            ;// throw new NotImplementedException();
        }

        /// <summary>
        /// Default value for upload URL is Pat's VM
        /// </summary>
        public override void SetDefault()
        {
            System.Diagnostics.Debug.WriteLine("UploadURLParameter::SetDefault start");
            Url = new Uri("http://pfet-v2.eecs.umich.edu:4908/img/");
            System.Diagnostics.Debug.WriteLine("UploadURLParameter::SetDefault end");
        }

        /// <summary>
        /// Save parameter to application settings.
        /// </summary>
        public override void Save()
        {
            System.Diagnostics.Debug.WriteLine("UploadURLParameter Save Request");
            if (DataContext.Settings.Contains(ParameterSettingName))
            {
                if ((Uri)DataContext.Settings[ParameterSettingName] != Url)
                {
                    System.Diagnostics.Debug.WriteLine("UploadURL::Save key existed and did not match. Updating");
                    DataContext.Settings[ParameterSettingName] = Url;
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine("UploadURL::Save key existed and matched");
                }
            }
            else
            {
                System.Diagnostics.Debug.WriteLine("UploadURL::Save adding new key");
                DataContext.Settings.Add(ParameterSettingName, Url);
            }
        }

        /// <summary>
        /// Load parameter from application settings.
        /// </summary>
        /// <returns>true if setting was loaded successfully, otherwise false.</returns>
        public override bool Load()
        {
            System.Diagnostics.Debug.WriteLine("UploadURLParameter Load Request");
            System.Diagnostics.Debug.WriteLine("ParameterSettingName: " + ParameterSettingName);
            bool ret = false;
            if (DataContext.Settings.Contains(ParameterSettingName))
            {
                Uri url = (Uri)DataContext.Settings[ParameterSettingName];
                this.Url = url;
                ret = true;
            }
            System.Diagnostics.Debug.WriteLine("UploadURLParameter Load Returning: " + ret.ToString());
            return ret;
        }
    }
}
