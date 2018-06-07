using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FrameAnalyser.dto
{
    class Frame
    {
        public int FrameNumber { get; set; }
        public List<Ball> Balls { get; set; }
    }
}
