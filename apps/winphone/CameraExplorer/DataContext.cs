/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.IO.IsolatedStorage;
using Windows.Phone.Media.Capture;

namespace CameraExplorer
{
    /// <summary>
    /// CameraExplorer.DataContext holds all application widely used instances, like parameters,
    /// camera instance and image memory stream.
    /// </summary>
    class DataContext : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        private static DataContext _singleton;
        private static IsolatedStorageSettings _settings = IsolatedStorageSettings.ApplicationSettings;
        private PhotoCaptureDevice _device = null;
        private ObservableCollection<Parameter> _parameters = new ObservableCollection<Parameter>();
        
        private UrlParameter _upload_url;

        /// <summary>
        /// Singleton instance accessor.
        /// </summary>
        public static DataContext Singleton
        {
            get
            {
                if (_singleton == null)
                {
                    _singleton = new DataContext();
                }

                return _singleton;
            }
        }

        /// <summary>
        /// Collection of camera parameters.
        /// </summary>
        public ObservableCollection<Parameter> Parameters
        {
            get
            {
                return _parameters;
            }

            private set
            {
                if (_parameters != value)
                {
                    _parameters = value;

                    if (PropertyChanged != null)
                    {
                        PropertyChanged(this, new PropertyChangedEventArgs("Parameters"));
                    }
                }
            }
        }

        public UrlParameter UploadUrl
        {
            get
            {
                return _upload_url;
            }
        }

        /// <summary>
        /// Camera instance. Setting new camera instance to this property causes the Parameters
        /// property to be updated as well with the new parameters from the new camera.
        /// </summary>
        public PhotoCaptureDevice Device
        {
            get
            {
                return _device;
            }

            set
            {
                if (_device != value)
                {
                    _device = value;
                    
                    if (_device != null)
                    {
                        ObservableCollection<Parameter> newParameters = new ObservableCollection<Parameter>();

                        Action<Parameter> addParameter = (Parameter parameter) =>
                        {
                            if (parameter.Supported && parameter.Modifiable)
                            {
                                try
                                {
                                    parameter.Refresh();
                                    parameter.SetSavedOrDefault();

                                    newParameters.Add(parameter);
                                }
                                catch (Exception)
                                {
                                    System.Diagnostics.Debug.WriteLine("Setting default to " + parameter.Name.ToLower() + " failed");
                                }
                            }
                            else
                            {
                                System.Diagnostics.Debug.WriteLine("Parameter " + parameter.Name.ToLower() + " is not supported or not modifiable");
                            }
                        };

                        addParameter(new SceneModeParameter(_device));
                        addParameter(new WhiteBalancePresetParameter(_device));
                        addParameter(new FlashModeParameter(_device));
                        addParameter(new FlashPowerParameter(_device));
                        addParameter(new IsoParameter(_device));
                        addParameter(new ExposureCompensationParameter(_device));
                        addParameter(new ExposureTimeParameter(_device));
                        addParameter(new AutoFocusRangeParameter(_device));
                        addParameter(new FocusIlluminationModeParameter(_device));
                        addParameter(new CaptureResolutionParameter(_device));

                        _upload_url = new UploadURLParameter(_device);
                        _upload_url.SetSavedOrDefault();

                        Parameters = newParameters;
                    }

                    if (PropertyChanged != null)
                    {
                        PropertyChanged(this, new PropertyChangedEventArgs("Device"));
                    }
                }
            }
        }

        /// <summary>
        /// Settings accessors.
        /// </summary>
        public static IsolatedStorageSettings Settings
        {
            get
            {
                return _settings;
            }
        }

        /// <summary>
        /// Memory stream to hold the image data captured in MainPage but consumed in PreviewPage.
        /// </summary>
        public MemoryStream ImageStream { get; set; }
    }
}