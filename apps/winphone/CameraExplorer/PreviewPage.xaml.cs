/*
 * Copyright © 2012-2013 Nokia Corporation. All rights reserved.
 * Nokia and Nokia Connecting People are registered trademarks of Nokia Corporation. 
 * Other product and company names mentioned herein may be trademarks
 * or trade names of their respective owners. 
 * See LICENSE.TXT for license information.
 */

using Microsoft.Phone.Controls;
using Microsoft.Xna.Framework.Media;
using System;
using System.IO.IsolatedStorage;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;

// REST Directives
using System.IO;
using System.Collections.Generic;
using System.Net;
using System.Text;

// https://gist.github.com/mcnemesis/6250994
namespace RESTAPI
{
    /// <summary>
    /// Encapsulates functionality to make it possible to make
    /// RESTful API calls on web resources and services
    /// </summary>
    class RESTAPIHandler
    {
        public delegate void RESTSuccessCallback(Stream stream);
        public delegate void RESTErrorCallback(String reason);

        public void get(Uri uri, Dictionary<String, String> extra_headers, RESTSuccessCallback success_callback, RESTErrorCallback error_callback)
        {
            HttpWebRequest request = WebRequest.CreateHttp(uri);

            if (extra_headers != null)
                foreach (String header in extra_headers.Keys)
                    try
                    {
                        request.Headers[header] = extra_headers[header];
                    }
                    catch (Exception) { }

            request.BeginGetResponse((IAsyncResult result) =>
            {
                HttpWebRequest req = result.AsyncState as HttpWebRequest;
                if (req != null)
                {
                    try
                    {
                        WebResponse response = req.EndGetResponse(result);
                        success_callback(response.GetResponseStream());
                    }
                    catch (WebException e)
                    {
                        error_callback(e.Message);
                        return;
                    }
                }
            }, request);
        }

        public static void post(Uri uri, Dictionary<String, String> post_params, Dictionary<String, String> extra_headers, RESTSuccessCallback success_callback, RESTErrorCallback error_callback)
        {
            HttpWebRequest request = WebRequest.CreateHttp(uri);
            request.ContentType = "application/x-www-form-urlencoded";
            request.Method = "POST";

            if (extra_headers != null)
                foreach (String header in extra_headers.Keys)
                    try
                    {
                        request.Headers[header] = extra_headers[header];
                    }
                    catch (Exception) { }


            request.BeginGetRequestStream((IAsyncResult result) =>
            {
                HttpWebRequest preq = result.AsyncState as HttpWebRequest;
                if (preq != null)
                {
                    Stream postStream = preq.EndGetRequestStream(result);

                    StringBuilder postParamBuilder = new StringBuilder();
                    if (post_params != null)
                        foreach (String key in post_params.Keys)
                            postParamBuilder.Append(String.Format("{0}={1}&", key, post_params[key]));

                    Byte[] byteArray = Encoding.UTF8.GetBytes(postParamBuilder.ToString());

                    postStream.Write(byteArray, 0, byteArray.Length);
                    postStream.Close();


                    preq.BeginGetResponse((IAsyncResult final_result) =>
                    {
                        HttpWebRequest req = final_result.AsyncState as HttpWebRequest;
                        if (req != null)
                        {
                            try
                            {
                                WebResponse response = req.EndGetResponse(final_result);
                                success_callback(response.GetResponseStream());
                            }
                            catch (WebException e)
                            {
                                error_callback(e.Message);
                                return;
                            }
                        }
                    }, preq);
                }
            }, request);
        }

        public static void post_image(Uri uri, Stream image_stream, RESTSuccessCallback success, RESTErrorCallback error)
        {
            HttpWebRequest request = WebRequest.CreateHttp(uri);
            request.ContentType = "image/jpeg";
            request.Method = "POST";

            request.BeginGetRequestStream((IAsyncResult result) =>
            {
                HttpWebRequest preq = result.AsyncState as HttpWebRequest;
                if (preq != null)
                {
                    Stream postStream = preq.EndGetRequestStream(result);

                    image_stream.CopyTo(postStream);
                    image_stream.Close();
                    postStream.Close();

                    preq.BeginGetResponse((IAsyncResult final_result) =>
                    {
                        HttpWebRequest req = final_result.AsyncState as HttpWebRequest;
                        if (req != null)
                        {
                            try
                            {
                                WebResponse response = req.EndGetResponse(final_result);
                                success(response.GetResponseStream());
                            }
                            catch (WebException e)
                            {
                                error(e.Message);
                                return;
                            }
                        }
                    }, preq);
                }
            }, request);
        }


        public static void upload_image(Uri uri, Stream image_stream)
        {
            System.Diagnostics.Debug.WriteLine("upload image start. uri: " + uri.ToString());
            try
            {
                var name = DateTime.Now.ToString("yyyy-MM-dd--HH-mm-ss-ff");
                uri = new Uri(uri.ToString() + name + ".jpg");
                System.Diagnostics.Debug.WriteLine(String.Format("About to upload {0} to {1}", name, uri.ToString()));
                RESTAPI.RESTAPIHandler.post_image(uri, image_stream, (stream) =>
                {
                    System.Diagnostics.Debug.WriteLine("Uploaded " + name + " successfully");
                },
                    (reason) =>
                    {
                        System.Diagnostics.Debug.WriteLine("Uploading " + name + " failed: " + reason.ToString());
                    }
                );
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("Uploading image failed: " + ex.HResult.ToString("x8") + " - " + ex.Message);
            }
        }
    }
}

namespace CameraExplorer
{
    /// <summary>
    /// Preview page displays the captured photo from DataContext.ImageStream and
    /// has a button to save the image to phone's camera roll.
    /// </summary>
    public partial class PreviewPage : PhoneApplicationPage
    {
        private CameraExplorer.DataContext _dataContext = CameraExplorer.DataContext.Singleton;
        private BitmapImage _bitmap = new BitmapImage();

        public PreviewPage()
        {
            InitializeComponent();

            DataContext = _dataContext;
        }

        /// <summary>
        /// When navigating to this page, DataContext.ImageStream will be set as the source
        /// for the Image control in XAML. If ImageStream is null, application will navigate
        /// directly back to the main page.
        /// </summary>
        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            if (_dataContext.ImageStream != null)
            {
                _bitmap.SetSource(_dataContext.ImageStream);
                image.Source = _bitmap;
            }
            else
            {
                NavigationService.GoBack();
            }

            base.OnNavigatedTo(e);
        }

        /// <summary>
        /// Clicking on the save button saves the photo in DataContext.ImageStream to media library
        /// camera roll. Once image has been saved, the application will navigate back to the main page.
        /// </summary>
        private void saveButton_Click(object sender, EventArgs e)
        {
            try
            {
                // Reposition ImageStream to beginning, because it has been read already in the OnNavigatedTo method.
                _dataContext.ImageStream.Position = 0;

                MediaLibrary library = new MediaLibrary();
                library.SavePictureToCameraRoll("CameraExplorer_" + DateTime.Now.ToString("yyyyMMddhhmmss") + ".jpg", _dataContext.ImageStream);
                
                // There should be no temporary file left behind
                using (var isolatedStorage = IsolatedStorageFile.GetUserStoreForApplication())
                {
                    var files = isolatedStorage.GetFileNames("CameraExplorer_*.jpg");
                    foreach (string file in files)
                    {
                        isolatedStorage.DeleteFile(file);
                        //System.Diagnostics.Debug.WriteLine("Temp file deleted: " + file);
                    }
                }

            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("Saving picture to camera roll failed: " + ex.HResult.ToString("x8") + " - " + ex.Message);
            }

            NavigationService.GoBack();
        }

        private void uploadButton_Click(object sender, EventArgs e)
        {
            try
            {
                // Reposition ImageStream to beginning, because it has been read already in the OnNavigatedTo method.
                System.Diagnostics.Debug.WriteLine("uploadButton_Click Before seeking image stream");
                _dataContext.ImageStream.Position = 0;

                System.Diagnostics.Debug.WriteLine("uploadButton_Click Before calling upload_image");
                RESTAPI.RESTAPIHandler.upload_image(_dataContext.UploadUrl.Url, _dataContext.ImageStream);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("Uploading from button click failed: " + ex.HResult.ToString("x8") + " - " + ex.Message);
            }

            NavigationService.GoBack();
        }
    }
}