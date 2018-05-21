using Accord.Video.FFMPEG;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
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

        string VideoPath = @"F:\Computer Vision\Computer-Vision-RNN\Videos\";
        string AnnotationPath = @"F:\Computer Vision\Computer-Vision-RNN\Anotations\";
        string FileName = "Training-5.mp4";

        List<dto.Frame> frames = new List<dto.Frame>();
        VideoFileReader vFReader = new VideoFileReader();
        int i = 0;

        private void Form1_Load(object sender, EventArgs e)
        {
            vFReader.Open(VideoPath + FileName);
            //frames = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Frame>>(File.ReadAllText(AnnotationPath + "video5_images.txt"));
            frames = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Frame>>(File.ReadAllText(@"F:\Computer Vision\Computer-Vision-RNN\FrameAnalyser\FrameAnalyser\bin\Debug\Images-Training-5.mp4\annotations.txt"));
        }

        private void button1_Click(object sender, EventArgs e)
        {
            i--;
            clear();
            update();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            i++;
            clear();
            update();
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
            if (i > vFReader.FrameCount)
            {
                i = (int)vFReader.FrameCount;
            }
            Bitmap bmpBaseOriginal = vFReader.ReadVideoFrame(i);
            pictureBox1.Image = bmpBaseOriginal;
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

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            vFReader.Close();
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            dto.Frame frame = null;
            dto.Ball ball = null;
            if (i >= 1 && frames.Count > i)
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
                    ball.Position = new dto.Point();
                    ball.Position.X = 1920 / 2;
                    ball.Position.Y = 1080 / 2;
                    ball.BoundingBox = new dto.Box();
                    ball.BoundingBox.Width = 80;
                    ball.BoundingBox.Height = 80;

                    e.SuppressKeyPress = true;
                    clear();
                    update();
                }
                return;
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
                    ball.BoundingBox.Width -= step;
                } else
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
                    ball.BoundingBox.Width += step;
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
        }

        private void ExportImages_Click(object sender, EventArgs e)
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

        private void ExportAnnotatedImages_Click(object sender, EventArgs e)
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

        private void SaveAnnotations_Click(object sender, EventArgs e)
        {
            File.WriteAllText(AnnotationPath + FileName + ".json", Newtonsoft.Json.JsonConvert.SerializeObject(frames));
        }

        private void button6_Click(object sender, EventArgs e)
        {
            foreach (string FileName in Directory.GetFiles(VideoPath))
            {
                vFReader.Open(FileName);

                string Name = FileName.Split('\\').Last();
                Name = Name.Split('.').First();

                if (!Directory.Exists(VideoPath + Name))
                    Directory.CreateDirectory(VideoPath + Name);
                else
                {
                    continue;
                }

                for (int i = 0; i < vFReader.FrameCount; i++)
                {
                    using (Bitmap bmpBaseOriginal = vFReader.ReadVideoFrame(i))
                    {
                        bmpBaseOriginal.Save(VideoPath + Name + "/Image" + i.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                    }
                }
            }
        }
    }
}
