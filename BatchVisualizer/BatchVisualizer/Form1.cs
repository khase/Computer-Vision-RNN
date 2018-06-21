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
            batches = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Batch>>(File.ReadAllText("../../../../RNN/AugmentedBatches.json"));
            //batches = Newtonsoft.Json.JsonConvert.DeserializeObject<List<dto.Batch>>(File.ReadAllText("Gelöscht.json"));
            hScrollBar1.Minimum = 0;
            hScrollBar1.Maximum = batches.Count+7;
        }

        private void update(dto.Batch batch)
        {
            Bitmap bmp = (Bitmap)pictureBox1.Image;
            if (bmp == null){
                bmp = new Bitmap(1920 * 2, 1080 * 2);
            }

            Point[] path = batch.Where(f => f != null).Select(f => f.Balls.First().Position).Select(p => new Point(p.X, p.Y)).ToArray();
            for (int i = path.Length - 1; i >= 0; i--)
            {
                for (int j = 0; j < i; j++)
                {
                    path[i] = new Point(path[i].X + path[j].X, path[i].Y + path[j].Y);
                }
            }
            path = path.Select(p => new Point(p.X + (1920), p.Y + (1080))).ToArray();

            //Point[] path = batch.Select(f => f.Balls.First().Position).Select(p => new Point(p.X + 1920, p.Y + 1080)).ToArray();

            Pen redPen = new Pen(Color.Red, 3);
            Pen greenPen = new Pen(Color.Green, 3);
            Pen bluePen = new Pen(Color.Blue, 3);
            using (var graphics = Graphics.FromImage(bmp))
            {
                graphics.Clear(Color.White);
                graphics.DrawLines(greenPen, path);
                foreach (Point p in path)
                {
                    graphics.DrawEllipse(bluePen, p.X - 2, p.Y - 2, 4, 4);
                }
            }
            pictureBox1.Image = bmp;
        }

        private void hScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {
            update(batches[e.NewValue]);
            textBox1.Text = ("Batch: " + e.NewValue + "Länge:" +  batches[e.NewValue].Count());
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private int testeBatches()
        {
            int zähler = 0;
            double faktor = 1.5;
            int absolut = 50;
            List<dto.Batch> batchesToDelete = new List<dto.Batch>();
            int i = 0;
            foreach (dto.Batch batch in batches)
            {
                double XactAbstand = -255;
                double YactAbstand = -255;
                double XlastAbstand = -255;
                double YlastAbstand = -255;
                bool runOnce = false;
                bool runTwice = false;
                FrameAnalyser.dto.Frame lastFrame = null;
                foreach (FrameAnalyser.dto.Frame frame in batch)
                {
                    if (lastFrame == null)
                    {
                        lastFrame = frame;
                        continue;
                    }
                    XactAbstand = lastFrame.Balls[0].Position.X - frame.Balls[0].Position.X;
                    YactAbstand = lastFrame.Balls[0].Position.Y - frame.Balls[0].Position.Y;
                    if ((Math.Abs(XactAbstand) > Math.Max((Math.Abs(XlastAbstand) * faktor), absolut)) || (Math.Abs(YactAbstand) > Math.Max((Math.Abs(YlastAbstand) * faktor), absolut)) && runTwice)
                    {
                        batchesToDelete.Add(batch);
                        zähler++;
                        break;
                    }
                    XlastAbstand = XactAbstand;
                    YlastAbstand = YactAbstand;
                    lastFrame = frame;
                    if (runOnce)
                        runTwice = true;
                    runOnce = true;
                }
                i++;
            }
            batches = batches.Except(batchesToDelete).ToList();
            File.WriteAllText("Gelöscht.json", Newtonsoft.Json.JsonConvert.SerializeObject(batchesToDelete, Newtonsoft.Json.Formatting.Indented));
            File.WriteAllText("../../../../RNN/AugmentedBatchesNew.json", Newtonsoft.Json.JsonConvert.SerializeObject(batches, Newtonsoft.Json.Formatting.Indented));
            hScrollBar1.Maximum = batches.Count;
            return zähler;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            MessageBox.Show(testeBatches().ToString() + " Batches gelöscht");
        }
    }
}