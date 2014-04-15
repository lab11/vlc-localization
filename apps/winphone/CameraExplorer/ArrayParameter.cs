/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

using Microsoft.Devices;
using Microsoft.Phone.Info;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using Windows.Phone.Media.Capture;

namespace CameraExplorer
{
    /// <summary>
    /// Enumerator to enumerate through ArrayParameterOptions in an ArrayParameter.
    /// </summary>
    public class ArrayParameterEnumerator : IEnumerator<ArrayParameterOption>
    {
        private ArrayParameter _arrayParameter;
        private int _count;
        private int _index = -1;

        public ArrayParameterEnumerator(ArrayParameter arrayParameter, int count)
        {
            _arrayParameter = arrayParameter;
            _count = count;
        }

        /// <summary>
        /// Current option.
        /// </summary>
        public object Current
        {
            get
            {
                return _arrayParameter.Option(_index);
            }
        }

        /// <summary>
        /// Current option.
        /// </summary>
        ArrayParameterOption IEnumerator<ArrayParameterOption>.Current
        {
            get
            {
                return (ArrayParameterOption)Current;
            }
        }

        /// <summary>
        /// Step forward one item.
        /// </summary>
        /// <returns></returns>
        public bool MoveNext()
        {
            if (_index < _count - 1)
            {
                _index++;

                return true;
            }
            else
            {
                return false;
            }
        }

        /// <summary>
        /// Reset to the beginning.
        /// </summary>
        public void Reset()
        {
            _index = -1;
        }

        public void Dispose()
        {
        }
    }

    /// <summary>
    /// ArrayParameterOption is a single item in an ArrayParameter.
    /// </summary>
    public class ArrayParameterOption
    {
        private dynamic _value;
        private string _name;
        private string _overlaySource;

        public ArrayParameterOption(dynamic value, string name, string overlaySource = null)
        {
            _value = value;
            _name = name;
            _overlaySource = overlaySource;
        }

        /// <summary>
        /// Camera property value related to this option.
        /// </summary>
        public dynamic Value
        {
            get
            {
                return _value;
            }
        }

        /// <summary>
        /// Name of this option.
        /// </summary>
        public string Name
        {
            get
            {
                return _name;
            }
        }

        /// <summary>
        /// Overlay icon path for this option.
        /// </summary>
        public string OverlaySource
        {
            get
            {
                return _overlaySource;
            }
        }
    }

    /// <summary>
    /// Abstract parameter base class for array type parameters.
    /// </summary>
    public abstract class ArrayParameter : Parameter, IReadOnlyCollection<ArrayParameterOption>
    {
        private List<ArrayParameterOption> _options = new List<ArrayParameterOption>();
        private ArrayParameterOption _selectedOption;
        private Guid _propertyId;
        private bool _refreshing = false;

        public ArrayParameter(PhotoCaptureDevice device, string name)
            : base(device, name)
        {
        }

        public ArrayParameter(PhotoCaptureDevice device, Guid propertyId, string name)
            : base(device, name)
        {
            _propertyId = propertyId;
        }

        /// <summary>
        /// Read parameter options and current value from Parameter.Device. Previous options
        /// are discarded and new options shall be created in the abstract void PopulateOptions()
        /// method.
        /// </summary>
        public override void Refresh()
        {
            _refreshing = true;

            _options.Clear();

            _selectedOption = null;

            try
            {
                PopulateOptions();

                Supported = _options.Count > 0;
            }
            catch (Exception)
            {
                Supported = false;

                System.Diagnostics.Debug.WriteLine("Getting " + Name.ToLower() + " failed");
            }

            Modifiable = Supported && _options.Count > 1;

            if (Supported)
            {
                NotifyPropertyChanged("Count");
                NotifyPropertyChanged("SelectedOption");
                NotifyPropertyChanged("OverlaySource");
            }

            _refreshing = false;
        }

        /// <summary>
        /// Get option for index.
        /// </summary>
        /// <param name="index">Option index</param>
        /// <returns>Option</returns>
        public ArrayParameterOption Option(int index)
        {
            return _options[index];
        }

        /// <summary>
        /// Current option.
        /// </summary>
        public ArrayParameterOption SelectedOption
        {
            get
            {
                return _selectedOption;
            }

            set
            {
                if (value == null) return; // null check to avoid http://stackoverflow.com/questions/3446102

                // value should not be saved when initialing the array
                bool save = _selectedOption != null;
                    
                if (_selectedOption != value)
                {
                    if (!(_refreshing && _selectedOption == null))
                    {
                        SetOption(value);
                    }

                    _selectedOption = value;

                    OverlaySource = _selectedOption.OverlaySource;

                    if (!(_refreshing && _selectedOption == null))
                    {
                        NotifyPropertyChanged("SelectedOption");
                        NotifyPropertyChanged("OverlaySource");
                    }

                    if (save)
                    {
                        Save();
                    }
                }
            }
        }

        /// <summary>
        /// Amount of options in this ArrayParameter.
        /// </summary>
        public int Count
        {
            get
            {
                return _options.Count;
            }
        }

        /// <summary>
        /// Get an enumerator to this ArrayParameter.
        /// </summary>
        /// <returns>Enumerator</returns>
        public IEnumerator<ArrayParameterOption> GetEnumerator()
        {
            return new ArrayParameterEnumerator(this, _options.Count);
        }

        /// <summary>
        /// Get an enumerator to this ArrayParameter.
        /// </summary>
        /// <returns>Enumerator</returns>
        IEnumerator IEnumerable.GetEnumerator()
        {
            return new ArrayParameterEnumerator(this, _options.Count);
        }

        /// <summary>
        /// Camera Guid that this ArrayParameter acts on.
        /// </summary>
        protected Guid PropertyId
        {
            get
            {
                return _propertyId;
            }
        }

        /// <summary>
        /// List of options for this ArrayParameter.
        /// </summary>
        protected List<ArrayParameterOption> Options
        {
            get
            {
                return _options;
            }
        }

        /// <summary>
        /// Abstract method to read the supported properties from the Parameter.Device.
        /// This method must populate the Options parameter with all the supported
        /// ArrayParameterOptions for the parameter in question. SelectedOption must be
        /// set as well.
        /// </summary>
        protected abstract void PopulateOptions();

        /// <summary>
        /// Abstract method to set a option as the current option. This method must set the
        /// Value from the ArrayParameterOption in an appropriate way to the Parameter.Device.
        /// </summary>
        /// <param name="option">Option to set</param>
        protected abstract void SetOption(ArrayParameterOption option);

        /// <summary>
        /// Set saved value if exists, otherwise set to default.
        /// </summary>
        public override void SetSavedOrDefault()
        {
            System.Diagnostics.Debug.WriteLine("Setting saved or default value to setting " + Name);
            if (!Load())
            {
                SetDefault();
            }
        }

        /// <summary>
        /// Save parameter to application settings.
        /// </summary>
        public override void Save()
        {
            if (SelectedOption == null || SelectedOption.Name == null || SelectedOption.Name.Length <= 0) return;

            if (DataContext.Settings.Contains(ParameterSettingName))
            {
                if ((string)DataContext.Settings[ParameterSettingName] != SelectedOption.Name)
                {
                    DataContext.Settings[ParameterSettingName] = SelectedOption.Name;
                }
            }
            else
            {
                DataContext.Settings.Add(ParameterSettingName, SelectedOption.Name);
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
                string name = DataContext.Settings[ParameterSettingName].ToString();
                for (int i = 0; i < Options.Count; i++)
                {
                    if (Options[i].Name.Equals(name))
                    {
                        ret = true;
                        SelectedOption = Options[i];
                    }
                }
            }
            return ret;
        }
    }

    /// <summary>
    /// Parameter to handle reading supported capture resolutions and changing the currently
    /// active capture resolution.
    /// </summary>
    public class CaptureResolutionParameter : ArrayParameter
    {
        public CaptureResolutionParameter(PhotoCaptureDevice device)
            : base(device, "Capture resolution")
        {
        }

        /// <summary>
        /// Reads supported capture resolutions from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// </summary>
        protected override void PopulateOptions()
        {
            IReadOnlyList<Windows.Foundation.Size> supportedValues = PhotoCaptureDevice.GetAvailableCaptureResolutions(Device.SensorLocation);
            Windows.Foundation.Size value = Device.CaptureResolution;

            ArrayParameterOption option = null;

            foreach (Windows.Foundation.Size i in supportedValues)
            {
                option = new ArrayParameterOption(i, i.Width + " x " + i.Height);

                Options.Add(option);

                if (i.Equals(value))
                {
                    SelectedOption = option;
                }
            }

            // The phone does support these resolutions, though it isn't given by the above? Aha:
            // http://developer.nokia.com/resources/library/Lumia/imaging/working-with-high-resolution-photos/capturing-high-resolution-photos.html
            var deviceName = DeviceStatus.DeviceName;
            if (deviceName.Contains("RM-875") || deviceName.Contains("RM-876") || deviceName.Contains("RM-877"))
            {
                Windows.Foundation.Size[] unofficialValues = { new Windows.Foundation.Size(7712, 4352), new Windows.Foundation.Size(7136, 5360) };
                foreach (Windows.Foundation.Size i in unofficialValues)
                {
                    option = new ArrayParameterOption(i, i.Width + " x " + i.Height);

                    Options.Add(option);

                    if (i.Equals(value))
                    {
                        SelectedOption = option;
                    }
                }
            }
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected async override void SetOption(ArrayParameterOption option)
        {
            if (Modifiable)
            {
                Modifiable = false;

                try
                {
                    await Device.SetCaptureResolutionAsync((Windows.Foundation.Size)option.Value);
                }
                catch (Exception e)
                {
                    System.Diagnostics.Debug.WriteLine("CaptureResolutionParameter::SetOption Exception: " + e.Message);
                }

                Modifiable = true;
            }
        }

        /// <summary>
        /// Default option for capture resolution is the first supported resolution.
        /// </summary>
        public override void SetDefault()
        {
            SelectedOption = Options.Count > 0 ? Options.First() : null;
        }
    }

    /// <summary>
    /// Parameter to handle reading supported exposure time values and changing the currently
    /// active exposure time.
    /// </summary>
    public class ExposureTimeParameter : ArrayParameter
    {
        public ExposureTimeParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.ExposureTime, "Exposure time")
        {
        }

        /// <summary>
        /// Reads supported exposure time values from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// 
        /// Exposure time auto value is set by setting the value in PhotoCaptureDevice API to
        /// null, therefore the separate handling for option "Auto".
        /// </summary>
        protected override void PopulateOptions()
        {
            ArrayParameterOption option = new ArrayParameterOption(null, "Auto", "Assets/Icons/overlay.exposuretime.auto.png");
            ArrayParameterOption selectedOption = option;

            Options.Add(option);

            CameraCapturePropertyRange range = PhotoCaptureDevice.GetSupportedPropertyRange(Device.SensorLocation, KnownCameraPhotoProperties.ExposureTime);
            object value = Device.GetProperty(PropertyId);
            // UInt32[] standardValues = { /* 16000, 8000, 4000,*/ 2000, 1000, 500, 250, 125, 60, 30, 15, 8, 4, 2 };
            UInt32[] standardValues = { 16666, 16000, 8000, 4000, 2000, 1000, 500, 250, 125, 60, 30, 15, 8, 4, 2 };

            UInt32 min = (UInt32)range.Min;
            UInt32 max = (UInt32)range.Max;
            System.Diagnostics.Debug.WriteLine(String.Format("Exposure time range (min {0}, max {1})", min, max));

            foreach (UInt32 i in standardValues)
            {
                UInt32 usecs = 1000000 / i;

                if (usecs >= min && usecs <= max)
                {
                    option = new ArrayParameterOption(usecs, "1 / " + i.ToString() + " s", "Assets/Icons/overlay.exposuretime." + i.ToString() + ".png");

                    Options.Add(option);

                    if (selectedOption == null && usecs.Equals(value))
                    {
                        selectedOption = option;
                    }
                }
            }

            // Expsoure times of 1 second and over are possible in some devices.
            UInt32 microseconds = 1000000; // second in microseconds
            while (microseconds <= max)
            {
                UInt32 usecs = microseconds / 1000000;
                option = new ArrayParameterOption(microseconds, usecs.ToString() + " s", "Assets/Icons/overlay.exposuretime." + usecs.ToString() + "s.png");

                Options.Add(option);

                if (selectedOption == null && usecs.Equals(value))
                {
                    selectedOption = option;
                }
                microseconds *= 2;
            }

            SelectedOption = selectedOption;
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected override void SetOption(ArrayParameterOption option)
        {
            Device.SetProperty(PropertyId, option.Value);
        }

        /// <summary>
        /// Default option for exposure time is the first supported value.
        /// </summary>
        public override void SetDefault()
        {
            SelectedOption = Options.Count > 0 ? Options.First() : null;
        }
    }

    /// <summary>
    /// Parameter to handle reading supported ISO values and changing the currently
    /// active ISO setting.
    /// </summary>
    public class IsoParameter : ArrayParameter
    {
        public IsoParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.Iso, "ISO")
        {
        }

        /// <summary>
        /// Reads supported ISO values from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// 
        /// ISO auto value is set by setting the value in PhotoCaptureDevice API to
        /// null, therefore the separate handling for option "Auto".
        /// </summary>
        protected override void PopulateOptions()
        {
            ArrayParameterOption option = new ArrayParameterOption(null, "Auto", "Assets/Icons/overlay.iso.auto.png");
            ArrayParameterOption selectedOption = option;

            Options.Add(option);

            CameraCapturePropertyRange range = PhotoCaptureDevice.GetSupportedPropertyRange(Device.SensorLocation, PropertyId);
            object value = Device.GetProperty(PropertyId);
            UInt32[] standardValues = { 100, 200, 400, 800, 1600, 3200 };

            UInt32 min = (UInt32)range.Min;
            UInt32 max = (UInt32)range.Max;

            foreach (UInt32 i in standardValues)
            {
                if (i >= min && i <= max)
                {
                    option = new ArrayParameterOption(i, "ISO " + i.ToString(), "Assets/Icons/overlay.iso." + i.ToString() + ".png");

                    Options.Add(option);

                    if (i.Equals(value))
                    {
                        selectedOption = option;
                    }
                }
            }

            SelectedOption = selectedOption;
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected override void SetOption(ArrayParameterOption option)
        {
            Device.SetProperty(PropertyId, option.Value);
        }

        /// <summary>
        /// Default option for ISO is the first supported value.
        /// </summary>
        public override void SetDefault()
        {
            SelectedOption = Options.Count > 0 ? Options.First() : null;
        }
    }

    /// <summary>
    /// Parameter to handle reading supported scene mode values and changing the currently
    /// active scene mode.
    /// </summary>
    public class SceneModeParameter : ArrayParameter
    {
        public SceneModeParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.SceneMode, "Scene mode")
        {
        }

        /// <summary>
        /// Reads supported scene mode values from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// </summary>
        protected override void PopulateOptions()
        {
            IReadOnlyList<object> supportedValues = PhotoCaptureDevice.GetSupportedPropertyValues(Device.SensorLocation, PropertyId);
            object value = Device.GetProperty(PropertyId);

            foreach (dynamic i in supportedValues)
            {
                CameraSceneMode csm = (CameraSceneMode)i;

                ArrayParameterOption option = new ArrayParameterOption(csm, csm.EnumerationToParameterName<CameraSceneMode>(), "Assets/Icons/overlay.scenemode." + csm.ToString().ToLower() + ".png");

                Options.Add(option);

                if (i.Equals(value))
                {
                    SelectedOption = option;
                }
            }
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected override void SetOption(ArrayParameterOption option)
        {
            Device.SetProperty(PropertyId, option.Value);
        }

        /// <summary>
        /// Default option for scene mode is either Auto if it is supported, or the last supported value.
        /// </summary>
        public override void SetDefault()
        {
            bool found = false;

            foreach (ArrayParameterOption i in Options)
            {
                if ((CameraSceneMode)i.Value == CameraSceneMode.Auto || i == Options.Last())
                {
                    SelectedOption = i;
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                SelectedOption = null;
            }
        }
    }

    /// <summary>
    /// Parameter to handle reading supported flash mode values and changing the currently
    /// active scene mode.
    /// </summary>
    public class FlashModeParameter : ArrayParameter
    {
        public FlashModeParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.FlashMode, "Flash mode")
        {
        }

        /// <summary>
        /// Reads supported flash mode values from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// </summary>
        protected override void PopulateOptions()
        {
            IReadOnlyList<object> supportedValues = PhotoCaptureDevice.GetSupportedPropertyValues(Device.SensorLocation, PropertyId);
            object value = Device.GetProperty(PropertyId);

            foreach (dynamic i in supportedValues)
            {
                FlashState fm = (FlashState)i;

                ArrayParameterOption option = new ArrayParameterOption(fm, fm.EnumerationToParameterName<FlashState>(), "Assets/Icons/overlay.flashmode." + fm.ToString().ToLower() + ".png");

                Options.Add(option);

                if (i.Equals(value))
                {
                    SelectedOption = option;
                }
            }
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected override void SetOption(ArrayParameterOption option)
        {
            Device.SetProperty(PropertyId, (FlashState)option.Value);
        }

        /// <summary>
        /// Default option for flash mode is either Auto if it is supported, or none.
        /// </summary>
        public override void SetDefault()
        {
            bool found = false;

            foreach (ArrayParameterOption i in Options)
            {
                if (i.Value == FlashState.Auto)
                {
                    SelectedOption = i;
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                SelectedOption = null;
            }
        }
    }

    /// <summary>
    /// Parameter to handle reading supported focus illumination mode values and changing the currently
    /// active focus illumination.
    /// </summary>
    public class FocusIlluminationModeParameter : ArrayParameter
    {
        public FocusIlluminationModeParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.FocusIlluminationMode, "Focus illumination mode")
        {
        }

        /// <summary>
        /// Reads supported focus illumination mode values from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// </summary>
        protected override void PopulateOptions()
        {
            IReadOnlyList<object> supportedValues = PhotoCaptureDevice.GetSupportedPropertyValues(Device.SensorLocation, PropertyId);
            object value = Device.GetProperty(PropertyId);

            foreach (dynamic i in supportedValues)
            {
                FocusIlluminationMode fim = (FocusIlluminationMode)i;

                ArrayParameterOption option = new ArrayParameterOption(fim, fim.EnumerationToParameterName<FocusIlluminationMode>());

                Options.Add(option);

                if (i.Equals(value))
                {
                    SelectedOption = option;
                }
            }
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected override void SetOption(ArrayParameterOption option)
        {
            Device.SetProperty(PropertyId, option.Value);
        }

        /// <summary>
        /// Default option for focus illumination mode is either Auto if it is supported, or none.
        /// </summary>
        public override void SetDefault()
        {
            bool found = false;

            foreach (ArrayParameterOption i in Options)
            {
                if (i.Value == FocusIlluminationMode.Auto)
                {
                    SelectedOption = i;
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                SelectedOption = null;
            }
        }
    }

    /// <summary>
    /// Parameter to handle reading supported white balance preset values and changing the currently
    /// active white balance preset.
    /// </summary>
    public class WhiteBalancePresetParameter : ArrayParameter
    {
        public WhiteBalancePresetParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraPhotoProperties.WhiteBalancePreset, "White balance preset")
        {
        }

        /// <summary>
        /// Reads supported white balance preset values from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// 
        /// White balace preset auto value is set by setting the value in PhotoCaptureDevice API to
        /// null, therefore the separate handling for option "Auto".
        /// </summary>
        protected override void PopulateOptions()
        {
            ArrayParameterOption option = new ArrayParameterOption(null, "Auto");
            ArrayParameterOption selectedOption = option;

            Options.Add(option);

            IReadOnlyList<object> supportedValues = PhotoCaptureDevice.GetSupportedPropertyValues(Device.SensorLocation, PropertyId);
            object value = Device.GetProperty(PropertyId);

            foreach (dynamic i in supportedValues)
            {
                WhiteBalancePreset wbp = (WhiteBalancePreset)i;

                option = new ArrayParameterOption(wbp, wbp.EnumerationToParameterName<WhiteBalancePreset>());

                Options.Add(option);

                if (i.Equals(value))
                {
                    selectedOption = option;
                }
            }

            SelectedOption = selectedOption;
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected override void SetOption(ArrayParameterOption option)
        {
            Device.SetProperty(PropertyId, option.Value);
        }

        /// <summary>
        /// Default option for white balance preset is the first supported value.
        /// </summary>
        public override void SetDefault()
        {
            SelectedOption = Options.Count > 0 ? Options.First() : null;
        }
    }

    /// <summary>
    /// Parameter to handle reading supported autofocus range values and changing the currently
    /// active white balance preset.
    /// </summary>
    public class AutoFocusRangeParameter : ArrayParameter
    {
        public AutoFocusRangeParameter(PhotoCaptureDevice device)
            : base(device, KnownCameraGeneralProperties.AutoFocusRange, "Auto focus range")
        {
        }

        /// <summary>
        /// Reads supported autofocus range values from Parameter.Device and populates
        /// ArrayParameter.Options accordingly. Sets the SelectedOption as well.
        /// </summary>
        protected override void PopulateOptions()
        {
            IReadOnlyList<object> supportedValues = PhotoCaptureDevice.GetSupportedPropertyValues(Device.SensorLocation, PropertyId);
            object value = Device.GetProperty(PropertyId);

            foreach (dynamic i in supportedValues)
            {
                AutoFocusRange afr = (AutoFocusRange)i;

                ArrayParameterOption option = new ArrayParameterOption(afr, afr.EnumerationToParameterName<AutoFocusRange>());

                Options.Add(option);

                if (i.Equals(value))
                {
                    SelectedOption = option;
                }
            }
        }

        /// <summary>
        /// The API response on querying whether the AutoFocusRange parameter is supported
        /// cannot be trusted on HTC devices at least, see http://bit.ly/11Midmq
        /// Until further notice we call the base Refresh implementation only for Nokia devices
        /// and asume the feature not to be supported on the other.
        /// </summary>
        public override void Refresh()
        {
            if (CultureInfo.InvariantCulture.CompareInfo.IndexOf(DeviceStatus.DeviceManufacturer, "Nokia", CompareOptions.IgnoreCase) == -1)
            {
                Supported = false;
                Modifiable = false;
                return;
            }

            base.Refresh();
        }

        /// <summary>
        /// Handles setting the given option as currently active one.
        /// </summary>
        /// <param name="option">Option to set as current value</param>
        protected override void SetOption(ArrayParameterOption option)
        {
            Device.SetProperty(PropertyId, option.Value);
        }

        /// <summary>
        /// Default option for autofocus range is either Normal if it is supported, or null.
        /// </summary>
        public override void SetDefault()
        {
            bool found = false;

            foreach (ArrayParameterOption i in Options)
            {
                if (i.Value == AutoFocusRange.Normal)
                {
                    SelectedOption = i;
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                SelectedOption = null;
            }
        }
    }
}