/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

using System.ComponentModel;
using Windows.Phone.Media.Capture;

namespace CameraExplorer
{
    /// <summary>
    /// Abstract base class for camera parameter handling.
    /// </summary>
    public abstract class Parameter : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        private PhotoCaptureDevice _device;
        private string _name;
        private string _overlaySource;
        private bool _supported = true;
        private bool _modifiable = true;

        protected Parameter(PhotoCaptureDevice device, string name)
        {
            _device = device;
            _name = name;
        }

        /// <summary>
        /// Derived parameter classes can use this method to notify about property changes.
        /// </summary>
        /// <param name="name"></param>
        protected void NotifyPropertyChanged(string name)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(name));
            }
        }

        /// <summary>
        /// PhotoCaptureDevice that this parameter was created from and will act on.
        /// </summary>
        public PhotoCaptureDevice Device
        {
            get
            {
                return _device;
            }
        }

        /// <summary>
        /// Name of the parameter to be displayed in the UI.
        /// </summary>
        public string Name
        {
            get
            {
                return _name;
            }
        }

        /// <summary>
        /// Name of the parameter in application settings.
        /// </summary>
        public string ParameterSettingName
        {
            get
            {
                if (Device.SensorLocation == CameraSensorLocation.Back)
                {
                    return "Back " + Name;
                }
                else
                {
                    return "Front " + Name;
                }
            }
        }

        /// <summary>
        /// Path to the overlay icon source used in viewfinder.
        /// </summary>
        public string OverlaySource
        {
            get
            {
                return _overlaySource;
            }

            protected set
            {
                if (_overlaySource != value)
                {
                    _overlaySource = value;

                    NotifyPropertyChanged("OverlaySource");
                }
            }
        }

        /// <summary>
        /// Is this parameter supported by the Device.
        /// </summary>
        public bool Supported
        {
            get
            {
                return _supported;
            }

            protected set
            {
                if (_supported != value)
                {
                    _supported = value;

                    NotifyPropertyChanged("Supported");
                }
            }
        }

        /// <summary>
        /// Is this parameter modifiable in the Device.
        /// </summary>
        public bool Modifiable
        {
            get
            {
                return _modifiable;
            }

            protected set
            {
                if (_modifiable != value)
                {
                    _modifiable = value;

                    NotifyPropertyChanged("Modifiable");
                }
            }
        }

        /// <summary>
        /// Read the parameter information from the Device.
        /// </summary>
        public abstract void Refresh();

        /// <summary>
        /// Set parameter default value.
        /// </summary>
        public abstract void SetDefault();

        /// <summary>
        /// Set parameter to saved or default value.
        /// </summary>
        public abstract void SetSavedOrDefault();

        /// <summary>
        /// Save parameter to application settings.
        /// </summary>
        public abstract void Save();

        /// <summary>
        /// Load parameter to application settings.
        /// </summary>
        /// <returns>true if setting was loaded successfully, otherwise false.</returns>
        public abstract bool Load();
    }
}