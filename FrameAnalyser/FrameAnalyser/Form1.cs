using Accord.Video.FFMPEG;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FrameAnalyser
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        string VideoPath = @"..\..\..\..\Videos\";
        string AnnotationPath = @"..\..\..\..\Anotations\";
        string FileName = "Training-5.mp4";

        List<dto.Frame> frames = new List<dto.Frame>();
        VideoFileReader vFReader = new VideoFileReader();
        int i = 0;
        Bitmap origFrame = null;

        private void Form1_Load(object sender, EventArgs e)
        {
            //vFReader.Open(VideoPath + FileName);
            //frames = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Frame>>(File.ReadAllText(AnnotationPath + FileName.Split('.').First()));

            // Fix JSON
            //foreach (string f in Directory.GetFiles(AnnotationPath, "*.json"))
            //{
            //    List<dto.Frame> tmp = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Frame>>(File.ReadAllText(f));
            //    for (int j = 0; j < tmp.Count; j++)
            //    {
            //        tmp[j].FrameNumber = j;
            //    }
            //    File.WriteAllText(f, Newtonsoft.Json.JsonConvert.SerializeObject(tmp, Newtonsoft.Json.Formatting.Indented));
            //}
        }

        private void prev_Click(object sender, EventArgs e)
        {
            if (vFReader != null && vFReader.IsOpen)
            {
                i--;
                loadFrame();
                clear();
                update();
            }
        }

        private void Next_Click(object sender, EventArgs e)
        {
            if (vFReader != null && vFReader.IsOpen)
            {
                i++;
                loadFrame();
                clear();
                update();
            }
        }

        private void update()
        {
            if (i >= 1 && frames.Count > i)
            {
                dto.Frame frame = frames[i - 1];
                overlay((Bitmap)pictureBox1.Image, frame);
            }
            else if (frames.Count <= i)
            {
                frames.Add(new dto.Frame());
            }
        }

        private void clear()
        {
            if (origFrame == null)
                return;
            pictureBox1.Image = (Bitmap)origFrame.Clone();
        }

        private void loadFrame()
        {
            if (i > vFReader.FrameCount - 1)
            {
                i = (int)vFReader.FrameCount - 1;
            }
            else if (i <= 0)
            {
                i = 1;
            }
            else
            {
                origFrame = vFReader.ReadVideoFrame(i);
            }
            this.Text = i + " / " + (vFReader.FrameCount - 1);
        }

        private Bitmap overlay(Bitmap bmp, dto.Frame frame)
        {
            if (bmp == null || frame == null)
                return bmp;
            Pen blackPen = new Pen(Color.Green, 3);
            using (var graphics = Graphics.FromImage(bmp))
            {
                if (frame.Balls != null && frame.Balls.Count > 0)
                {
                    dto.Ball ball = frame.Balls[0];
                    graphics.DrawRectangle(blackPen, new Rectangle(new Point(ball.Position.X - (ball.BoundingBox.Width / 2), ball.Position.Y - (ball.BoundingBox.Height / 2)), new Size(ball.BoundingBox.Width, ball.BoundingBox.Height)));
                }
            }
            return bmp;
        }

        private unsafe Rectangle FindBall(Bitmap source)
        {
            int bitsPerPixel = 24;
            BitmapData bData = source.LockBits(new Rectangle(0, 0, source.Width, source.Height), ImageLockMode.ReadWrite, source.PixelFormat);

            /*This time we convert the IntPtr to a ptr*/
            byte* scan0 = (byte*)bData.Scan0.ToPointer();

            List<Point> ballPixels = new List<Point>();

            for (int i = 0; i < bData.Height; ++i)
            {
                for (int j = 0; j < bData.Width; ++j)
                {
                    byte* data = scan0 + i * bData.Stride + j * bitsPerPixel / 8;
                    byte* r = data;
                    byte* g = data + 1;
                    byte* b = data + 2;
                    Color col = Color.FromArgb(*r, *g, *b);
                    float hue = col.GetHue();
                    float saturation = col.GetSaturation();
                    float value = col.GetBrightness();

                    if (saturation > 0.2)
                    {
                        ballPixels.Add(new Point(j, i));
                    }
                    else
                    {
                        *r = 0;
                        *g = 0;
                        *b = 0;
                    }
                }
            }
            source.UnlockBits(bData);

            int minX = ballPixels.Select(p => p.X).OrderBy(x => x).Skip(100).Min() - 2;
            int maxX = ballPixels.Select(p => p.X).OrderByDescending(x => x).Skip(100).Max() + 2;
            int minY = ballPixels.Select(p => p.Y).OrderBy(y => y).Skip(100).Min() - 2;
            int maxY = ballPixels.Select(p => p.Y).OrderByDescending(y => y).Skip(100).Max() + 2;

            return new Rectangle(new Point(minX, minY), new Size(maxX - minX, maxY - minY));
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (vFReader != null && vFReader.IsOpen)
            {
                vFReader.Close();
            }
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            dto.Frame frame = null;
            dto.Ball ball = null;
            if (i >= 1 && frames != null && frames.Count > i)
            {
                frame = frames[i - 1];
                if (frame.Balls.Count > 0)
                {
                    ball = frame.Balls[0];
                }
            }
            if (ball == null)
            {
                if (e.KeyCode == Keys.NumPad5)
                {
                    frame.Balls.Add(new dto.Ball());
                    ball = frame.Balls[0];
                    Rectangle rect = FindBall(origFrame);
                    if (rect != null)
                    {
                        ball.Position = new dto.Point();
                        ball.Position.X = rect.X + (rect.Width / 2);
                        ball.Position.Y = rect.Y + (rect.Height / 2);
                        ball.BoundingBox = new dto.Box();
                        ball.BoundingBox.Width = rect.Width;
                        ball.BoundingBox.Height = rect.Height;
                    }
                    else if (i >= 2 && frames[i - 2] != null && frames[i - 2].Balls.Count > 0)
                    {
                        dto.Ball lastBall = frames[i - 2].Balls[0];
                        ball.Position = new dto.Point();
                        ball.Position.X = lastBall.Position.X;
                        ball.Position.Y = lastBall.Position.Y;
                        ball.BoundingBox = new dto.Box();
                        ball.BoundingBox.Width = lastBall.BoundingBox.Width;
                        ball.BoundingBox.Height = lastBall.BoundingBox.Height;
                    }
                    else
                    {
                        ball.Position = new dto.Point();
                        ball.Position.X = 1920 / 2;
                        ball.Position.Y = 1080 / 2;
                        ball.BoundingBox = new dto.Box();
                        ball.BoundingBox.Width = 80;
                        ball.BoundingBox.Height = 80;
                    }

                    e.SuppressKeyPress = true;
                    clear();
                    update();
                }
                return;
            }
            if (e.KeyCode == Keys.Delete)
            {
                if (frame.Balls != null && frame.Balls.Count > 0)
                {
                    frame.Balls.RemoveAt(0);
                    e.SuppressKeyPress = true;
                    clear();
                    update();
                }
            }
            int step = 1;
            if (e.Control)
            {
                step = 15;
            }
            if (e.KeyCode == Keys.NumPad6)
            {
                if (e.Alt)
                {
                    ball.BoundingBox.Width += step;
                }
                else
                {
                    ball.Position.X += step;
                }
                e.SuppressKeyPress = true;
                clear();
                update();
            }
            else if (e.KeyCode == Keys.NumPad4)
            {
                if (e.Alt)
                {
                    ball.BoundingBox.Width -= step;
                }
                else
                {
                    ball.Position.X -= step;
                }
                e.SuppressKeyPress = true;
                clear();
                update();
            }
            else if (e.KeyCode == Keys.NumPad8)
            {
                if (e.Alt)
                {
                    ball.BoundingBox.Height += step;
                }
                else
                {
                    ball.Position.Y -= step;
                }
                e.SuppressKeyPress = true;
                clear();
                update();
            }
            else if (e.KeyCode == Keys.NumPad2)
            {
                if (e.Alt)
                {
                    ball.BoundingBox.Height -= step;
                }
                else
                {
                    ball.Position.Y += step;
                }
                e.SuppressKeyPress = true;
                clear();
                update();
            }
            else if (e.KeyCode == Keys.A)
            {
                prev_Click(null, null);
            }
            else if (e.KeyCode == Keys.D)
            {
                Next_Click(null, null);
            }
        }

        private void ExportImages_Click(object sender, EventArgs e)
        {
            if (vFReader != null && vFReader.IsOpen)
            {
                if (!Directory.Exists("Images-" + FileName))
                    Directory.CreateDirectory("Images-" + FileName);

                for (int i = 0; i < vFReader.FrameCount; i++)
                {
                    using (Bitmap bmpBaseOriginal = vFReader.ReadVideoFrame(i))
                    {
                        bmpBaseOriginal.Save("Images-" + FileName + "/Image" + i.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                    }
                }
            }
        }

        private void ExportAnnotatedImages_Click(object sender, EventArgs e)
        {
            if (vFReader != null && vFReader.IsOpen)
            {
                if (!Directory.Exists("AnnotatedImages-" + FileName))
                    Directory.CreateDirectory("AnnotatedImages-" + FileName);

                for (int i = 0; i < vFReader.FrameCount; i++)
                {
                    using (Bitmap bmpBaseOriginal = vFReader.ReadVideoFrame(i))
                    {
                        if (i >= 1 && frames.Count > i)
                        {
                            dto.Frame frame = frames[i];
                            overlay(bmpBaseOriginal, frame).Save("AnnotatedImages-" + FileName + "/AnnotatedImage" + i.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                        }
                        else if (frames.Count <= i)
                        {
                            frames.Add(new dto.Frame());
                        }
                    }
                }
            }
        }

        private void SaveAnnotations_Click(object sender, EventArgs e)
        {
            if (vFReader != null && vFReader.IsOpen)
            {
                // Fix JSON
                //for (int j = 0; j < frames.Count; j++)
                //{
                //    frames[j].FrameNumber = j;
                //}
                File.WriteAllText(AnnotationPath + FileName.Split('.').First() + ".json", Newtonsoft.Json.JsonConvert.SerializeObject(frames.Where(f => f.Balls != null), Newtonsoft.Json.Formatting.Indented));
            }
        }

        private void Form1_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop)) e.Effect = DragDropEffects.Copy;
        }

        private void Form1_DragDrop(object sender, DragEventArgs e)
        {
            string[] files = (string[])e.Data.GetData(DataFormats.FileDrop);

            FileInfo fi = new FileInfo(files[0]);
            VideoPath = fi.DirectoryName + "\\";
            AnnotationPath = VideoPath.Replace("Videos", "Anotations");
            FileName = fi.Name;

            vFReader.Open(VideoPath + FileName);
            FileInfo tInfo = new FileInfo(AnnotationPath + FileName.Split('.').First() + ".json");
            FileInfo pInfo = new FileInfo(AnnotationPath + FileName.Split('.').First().Replace("Training", "Prediction") + ".json");
            if (pInfo.Exists)
            {
                if (MessageBox.Show("Prediction-File found, wan't to load it?", "Prediction", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    frames = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Frame>>(File.ReadAllText(pInfo.FullName));
                }
                else if (tInfo.Exists)
                {
                    frames = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Frame>>(File.ReadAllText(tInfo.FullName));
                }
            }
            else if (tInfo.Exists)
            {
                frames = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Frame>>(File.ReadAllText(tInfo.FullName));
            }
            i = 1;
            loadFrame();
            clear();
            update();
        }
    }
}
