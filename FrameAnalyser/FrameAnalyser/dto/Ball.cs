using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FrameAnalyser.dto
{
    class Ball
    {

        public int Tag { get; set; }
        public Point Position { get; set; }
        public Box BoundingBox { get; set; }
    }
}
