/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

using Microsoft.Devices;
using Microsoft.Phone.Shell;
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using Windows.Phone.Media.Capture;

namespace CameraExplorer
{
    /// <summary>
    /// Abstract parameter base class for range type parameters.
    /// </summary>
    /// <typeparam name="T">Type of the parameter minimum, maximum and value.</typeparam>
    public abstract class RangeParameter<T> : Parameter
    {
        private Guid _propertyId;
        private T _value;
        private T _minimum;
        private T _maximum;

        protected RangeParameter(PhotoCaptureDevice device, Guid propertyId, string name)
            : base(device, name)
        {
            _propertyId = propertyId;

            Refresh();
        }

        /// <summary>
        /// Reads the range minimum, maximum and current value. Sets Supported and Modifiable
        /// appropriately.
        /// </summary>
        public override void Refresh()
        {
            try
            {
                CameraCapturePropertyRange range = PhotoCaptureDevice.GetSupportedPropertyRange(Device.SensorLocation, _propertyId);

                if (range == null)
                {
                    Supported = false;
                }
                else
                {
                    Minimum = (T)range.Min;
                    Maximum = (T)range.Max;
                    _value = (T)Device.GetProperty(_propertyId);
                    Supported = true;
                }
            }
            catch (Exception)
            {
                Supported = false;

                System.Diagnostics.Debug.WriteLine("Getting " + Name.ToLower() + " failed");
            }

            Modifiable = Supported && !_minimum.Equals(_maximum);

            if (Supported)
            {
                NotifyPropertyChanged("Value");
                NotifyPropertyChanged("OverlaySource");
            }
        }

        /// <summary>
        /// Range minimum value.
        /// </summary>
        public T Minimum
        {
            get
            {
                return _minimum;
            }

            private set
            {
                if (!_minimum.Equals(value))
                {
                    _minimum = value;

                    NotifyPropertyChanged("Minimum");
                }
            }
        }

        /// <summary>
        /// Range maximum value.
        /// </summary>
        public T Maximum
        {
            get
            {
                return _maximum;
            }

            private set
            {
                if (!_maximum.Equals(value))
                {
                    _maximum = value;

                    NotifyPropertyChanged("Maximum");
                }
            }
        }

        /// <summary>
        /// Range current value.
        /// </summary>
        public T Value
        {
            get
            {
                return _value;
            }

            set
            {
                if (!_value.Equals(value))
                {
                    try
                    {
                        _value = value;

                        Device.SetProperty(_propertyId, (T)value);

                        NotifyPropertyChanged("Value");

                        Save();
                    }
                    catch (Exception)
                    {
                        System.Diagnostics.Debug.WriteLine("Setting " + Name.ToLower() + " failed");
                    }
                }
            }
        }

        /// <summary>
        /// Set saved value if exists, otherwise set to default.
        /// </summary>
        public override void SetSavedOrDefault()
        {
            if (!Load())
            {
                SetDefault();
            }
        }
    }

    /// <summary>
    /// Exposure compensation parameter, acts on KnownCameraPhotoProperties.ExposureCompensation.
    /// </summary>
    public class ExposureCompensationParameter : RangeParameter<Int32>
    {
        public ExposureCompensationParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.ExposureCompensation, "Exposure compensation")
        {
        }

        /// <summary>
        /// Default value for exposure compensation is the middle value in the supported range.
        /// </summary>
        public override void SetDefault()
        {
            Value = (Int32)(Minimum + (Maximum - Minimum) / 2);
        }

        /// <summary>
        /// Save parameter to application settings.
        /// </summary>
        public override void Save()
        {
            if (DataContext.Settings.Contains(ParameterSettingName))
            {
                if ((Int32)DataContext.Settings[ParameterSettingName] != Value)
                {
                    DataContext.Settings[ParameterSettingName] = Value;
                }
            }
            else
            {
                DataContext.Settings.Add(ParameterSettingName, Value);
            }
        }

        /// <summary>
        /// Load parameter from application settings.
        /// </summary>
        /// <returns>true if setting was loaded successfully, otherwise false.</returns>
        public override bool Load()
        {
            bool ret = false;

            if (DataContext.Settings.Contains(ParameterSettingName))
            {
                Int32 value = (Int32)DataContext.Settings[ParameterSettingName];
                this.Value = value;
                ret = true;
            }
            return ret;
        }
    }

    /// <summary>
    /// Exposure compensation parameter, acts on KnownCameraPhotoProperties.FlashPower.
    /// </summary>
    public class FlashPowerParameter : RangeParameter<UInt32>
    {
        public FlashPowerParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.FlashPower, "Flash power")
        {
        }

        /// <summary>
        /// Default value for flash power is the middle value in the supported range.
        /// </summary>
        public override void SetDefault()
        {
            Value = (UInt32)(Minimum + (Maximum - Minimum) / 2);
        }

        /// <summary>
        /// Save parameter to application settings.
        /// </summary>
        public override void Save()
        {
            if (DataContext.Settings.Contains(ParameterSettingName))
            {
                if ((UInt32)DataContext.Settings[ParameterSettingName] != Value)
                {
                    DataContext.Settings[ParameterSettingName] = Value;
                }
            }
            else
            {
                DataContext.Settings.Add(ParameterSettingName, Value);
            }
        }

        /// <summary>
        /// Load parameter from application settings.
        /// </summary>
        /// <returns>true if setting was loaded successfully, otherwise false.</returns>
        public override bool Load()
        {
            bool ret = false;

            if (DataContext.Settings.Contains(ParameterSettingName))
            {
                UInt32 value = (UInt32)DataContext.Settings[ParameterSettingName];
                this.Value = value;
                ret = true;
            }
            return ret;
        }
    }
}