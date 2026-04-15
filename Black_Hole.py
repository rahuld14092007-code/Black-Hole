import moderngl_window as mglw
import numpy as np
import math

class GargantuaFinal(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Gargantua Final: Volumetric Particle Flow"
    window_size = (1920, 1080)
    aspect_ratio = 16 / 9
    cursor = False 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.program = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_position;
                out vec2 uv;
                void main() {
                    uv = in_position;
                    gl_Position = vec4(in_position, 0.0, 1.0);
                }
            ''',
            fragment_shader=self.get_fragment_shader()
        )
        vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype='f4')
        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, 'in_position')

        # Initial Flight State
        self.camera_pos = np.array([0.0, 1.5, -25.0], dtype=np.float32)
        self.camera_yaw = math.pi / 2.0
        self.camera_pitch = -0.05
        self.zoom = 1.8
        self.mouse_sens = 0.0012
        self.keys = set()
        self.mode = 1.0

    def on_render(self, time, frame_time):
        self.ctx.clear()
        dt_speed = 20.0 * frame_time 
        
        # Calculate Forward/Right/Up vectors for movement
        f = np.array([math.cos(self.camera_yaw)*math.cos(self.camera_pitch), math.sin(self.camera_pitch), math.sin(self.camera_yaw)*math.cos(self.camera_pitch)])
        f /= np.linalg.norm(f)
        r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r)
        u = np.cross(r, f)

        if self.wnd.keys.W in self.keys: self.camera_pos += f * dt_speed
        if self.wnd.keys.S in self.keys: self.camera_pos -= f * dt_speed
        if self.wnd.keys.A in self.keys: self.camera_pos -= r * dt_speed
        if self.wnd.keys.D in self.keys: self.camera_pos += r * dt_speed
        if self.wnd.keys.E in self.keys: self.camera_pos += u * dt_speed
        if self.wnd.keys.Q in self.keys: self.camera_pos -= u * dt_speed

        # Send Data to GPU
        self.program['iTime'].value = time
        self.program['camPos'].value = tuple(self.camera_pos)
        self.program['camDir'].value = tuple(f)
        self.program['zoom'].value = self.zoom
        self.program['bhMode'].value = self.mode
        self.program['iRes'].value = (self.window_size[0], self.window_size[1])
        self.vao.render(mode=self.ctx.TRIANGLE_STRIP)

    def on_mouse_drag_event(self, x, y, dx, dy):
        self.camera_yaw += dx * self.mouse_sens
        self.camera_pitch -= dy * self.mouse_sens
        self.camera_pitch = np.clip(self.camera_pitch, -1.5, 1.5)

    def on_mouse_scroll_event(self, x, y):
        self.zoom = np.clip(self.zoom + y * 0.1, 0.5, 12.0)

    def on_key_event(self, key, action, mods):
        if action == self.wnd.keys.ACTION_PRESS:
            self.keys.add(key)
            if key == self.wnd.keys.NUMBER_1: self.mode = 1.0
            if key == self.wnd.keys.NUMBER_2: self.mode = 2.0
            if key == self.wnd.keys.NUMBER_3: self.mode = 3.0
            if key == self.wnd.keys.R: self.camera_pos = np.array([0.0, 1.5, -25.0])
            if key == self.wnd.keys.ESCAPE: self.wnd.close()
        elif action == self.wnd.keys.ACTION_RELEASE: self.keys.discard(key)

    def get_fragment_shader(self):
        return '''
        #version 330
        in vec2 uv;
        out vec4 fragColor;
        uniform float iTime, zoom, bhMode;
        uniform vec3 camPos, camDir;
        uniform vec2 iRes;

        #define RS 1.2
        #define STEPS 450

        // High-frequency hash for pinpoint stars
        float hash(vec3 p) {
            p = fract(p * 0.1031); p += dot(p, p.yzx + 33.33);
            return fract((p.x + p.y) * p.z);
        }

        // Multi-layered noise for "moving gas"
        float noise(vec3 x) {
            vec3 i = floor(x); vec3 f = fract(x);
            f = f*f*(3.0-2.0*f);
            return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
                       mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);
        }

        void main() {
            vec2 p = uv * vec2(iRes.x/iRes.y, 1.0);
            vec3 ww = normalize(camDir);
            vec3 uu = normalize(cross(ww, vec3(0,1,0)));
            vec3 vv = normalize(cross(uu, ww));
            vec3 rd = normalize(p.x*uu + p.y*vv + zoom*ww);
            
            vec3 rp = camPos, rd_curr = rd, acc = vec3(0.0);
            float minR = 100.0, dt = 0.14;
            bool hit = false;

            for(int i=0; i<STEPS; i++) {
                float r = length(rp);
                minR = min(minR, r);
                if(r < RS) { hit = true; break; }
                if(r > 80.0) break;

                // Spacetime Curvature (Bending)
                float bend = (1.5 * RS) / (r * r);
                rd_curr = normalize(rd_curr - (rp/r) * bend * dt);
                
                // Gas Particle Movement Logic
                if(bhMode < 2.5) {
                    float h = 0.05 + (r-2.0)*0.012; // Very thin accretion disk
                    if(abs(rp.y) < h && r > 2.2 && r < 18.0) {
                        // Keplerian velocity: Speed increases closer to center
                        float orbitalVel = 3.5 / sqrt(r); 
                        float angle = atan(rp.z, rp.x) + iTime * orbitalVel;
                        
                        // Sample noise at high frequency to look like particles
                        vec3 particlePos = vec3(cos(angle)*r, rp.y*25.0, sin(angle)*r);
                        float d = noise(particlePos * 4.0) * noise(particlePos * 0.5);
                        
                        // Doppler Beaming (Relativistic brightness)
                        vec3 vel = normalize(vec3(-rp.z, 0, rp.x));
                        float doppler = pow(1.1 + dot(rd_curr, vel), 4.0);
                        
                        // Color Selection
                        vec3 colBase = (bhMode == 1.0) ? vec3(1.0, 0.4, 0.05) : vec3(0.2, 0.5, 1.0);
                        float edgeFade = smoothstep(18.0, 14.0, r) * smoothstep(2.0, 3.0, r);
                        acc += colBase * d * doppler * edgeFade * dt * 4.5;
                    }
                }
                rp += rd_curr * dt;
                dt = min(0.14, r * 0.045);
            }

            vec3 final = acc;
            if(!hit) {
                // Photon Ring (Einstein Ring)
                float ring = pow(RS/minR, 35.0);
                final += vec3(1.0, 0.9, 0.7) * ring * 0.6;
                
                // Pure Black Background + Precision Stars
                float s = pow(hash(floor(rd_curr * 1200.0)), 150.0);
                final += vec3(s) * 3.5;
            }

            // Cinematic ACES Tonemapping
            final = clamp(final, 0.0, 1.0);
            final = (final*(2.51*final+0.03))/(final*(2.43*final+0.59)+0.14);
            fragColor = vec4(pow(final, vec3(1.0/2.2)), 1.0);
        }
        '''

if __name__ == '__main__':
    GargantuaFinal.run()