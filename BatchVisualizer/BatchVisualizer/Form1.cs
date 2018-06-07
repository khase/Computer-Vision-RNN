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

namespace BatchVisualizer
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        List<dto.Batch> batches;

        private void Form1_Load(object sender, EventArgs e)
        {
            batches = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Batch>>(File.ReadAllText("../../../../RNN/Batches.json"));
            hScrollBar1.Minimum = 0;
            hScrollBar1.Maximum = batches.Count;
        }

        private void update(dto.Batch batch)
        {
            Bitmap bmp = (Bitmap)pictureBox1.Image;
            if (bmp == null){
                bmp = new Bitmap(1920 * 2, 1080 * 2);
            }

            //Point[] path = batch.Select(f => f.Balls.First().Position).Select(p => new Point(p.X, p.Y)).ToArray();
            //for (int i = path.Length - 1; i >= 0; i--)
            //{
            //    for (int j = 0; j < i; j++)
            //    {
            //        path[i] = new Point(path[i].X + path[j].X, path[i].Y + path[j].Y);
            //    }
            //}
            //path = path.Select(p => new Point(p.X + (1920), p.Y + (1080))).ToArray();

            Point[] path = batch.Select(f => f.Balls.First().Position).Select(p => new Point(p.X + 1920, p.Y + 1080)).ToArray();

            Pen redPen = new Pen(Color.Red, 3);
            Pen greenPen = new Pen(Color.Green, 3);
            Pen bluePen = new Pen(Color.Blue, 3);
            using (var graphics = Graphics.FromImage(bmp))
            {
                graphics.Clear(Color.White);
                graphics.DrawLines(greenPen, path);
            }
            pictureBox1.Image = bmp;
        }

        private void hScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {
            update(batches[e.NewValue]);
        }
    }
}
