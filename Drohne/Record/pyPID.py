"""
Python-PID-Regler v1.0
Einfacher PID-Regler, wird zunächst mit fünf Parametern konfiguriert, und dann benutzt um einen Regelwert für gegebenen Soll- und Istwert auszugeben

Inputs (setup):
- kp, ki, kd; die Vorfaktoren der jeweiligen Anteile (P,I,D)
- dr ist der Schrittbereich (größtmöglicher Schritt) und dt der kleinstmögliche Schritt

Inputs:
- Sollwert und Istwert
Output:
- Regelwert

author  = "Vondracek, Niclas", "Schwarz, Martin", "Haberkorn, Lukas"
contact = "nvondracek@stud.hs-bremen.de", "maschwarz@stud.hs-bremen.de", "lhaberkorn@stud.hs-bremen.de"
data    = date = "2023/12/21"
deprecated = false
status = "Release"
version = "1.0"
"""
#----------------------------------------------------------------------------------------------------------------------------------------
class pyPID :
  dt  = 0.0
  dr  = 0.0
  kp  = 0.0
  kd  = 0.0
  ki  = 0.0
  err = 0.0
  int = 0.0
  def __init__(self, dt, dr, kp, ki, kd) :
    self.dt  = dt
    self.max = dr
    self.min = -dr
    self.kp  = kp
    self.ki  = ki
    self.kd  = kd

  def run(self,ed,st) :
    error = ed - st;

    # P Anteil
    P = self.kp * error;

    # I Anteil
    self.int += error * self.dt;
    I = self.ki * self.int;
    
    # D Anteil
    D = self.kd * (error - self.err) / self.dt;
 
    output = P + I + D;

    if output > self.max :
        output = self.max
    elif output < self.min :
        output = self.min

    self.err = error;
    return(output)
